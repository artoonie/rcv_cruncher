"""Run one rcv_cruncher batch job in a directory. Shared by the Pyodide worker and serve.py.

The caller writes the CVR files under ``<job_dir>/cvr/`` first, with paths matching the
``cvr_path`` column of the contest set. This module then writes contest_set.csv and
run_config.json, runs the batch pipeline exactly as the CLI does, and zips the outputs.
"""
import contextlib
import csv
import io
import json
import pathlib
import platform
import traceback
import zipfile

OUTPUT_DIRS = ("results", "converted_cvr")


def run_job(job_dir, contest_set_csv: str, run_config_json: str, capture_log: bool = False) -> dict:
    """``capture_log`` collects stdout/stderr into the result instead of letting it stream (used by serve.py;
    under Pyodide the worker streams them to the page as they happen)."""
    job_dir = pathlib.Path(job_dir)
    cvr_root = job_dir / "cvr"
    cvr_root.mkdir(parents=True, exist_ok=True)

    (job_dir / "contest_set.csv").write_text(contest_set_csv, encoding="utf-8")
    run_config = json.loads(run_config_json or "{}")
    run_config["cvr_path_root"] = str(cvr_root)
    (job_dir / "run_config.json").write_text(json.dumps(run_config, indent=4), encoding="utf-8")

    if platform.system() == "Emscripten":
        # no threads in the browser: stop tqdm trying to start its monitor thread
        import tqdm

        tqdm.tqdm.monitor_interval = 0

    error = None
    n_contests = 0
    log = io.StringIO()
    with contextlib.ExitStack() as stack:
        if capture_log:
            stack.enter_context(contextlib.redirect_stdout(log))
            stack.enter_context(contextlib.redirect_stderr(log))
        try:
            import rcv_cruncher.batch as batch

            contest_set, config = batch._read_contest_set(job_dir)
            n_contests = len(contest_set)
            batch._crunch_contest_set(contest_set, config, job_dir, fresh_output=True)
        except Exception:  # surfaced to the UI; per-contest errors are already in results/error_log.csv
            error = traceback.format_exc()

    files = []
    for out in OUTPUT_DIRS:
        for p in sorted((job_dir / out).rglob("*")):
            if p.is_file():
                files.append({"path": str(p.relative_to(job_dir)), "size": p.stat().st_size})

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(job_dir / f["path"], f["path"])
    (job_dir / "results.zip").write_bytes(buf.getvalue())

    # per-contest failures are logged by batch.py; error_log_EMPTY.csv is written when there were none
    error_log = job_dir / "results" / "error_log.csv"
    errors = []
    if error_log.exists():
        with open(error_log, encoding="utf-8", newline="") as f:
            errors = [{"contest": r.get("contest", ""), "step": r.get("cruncher_step", ""), "message": r.get("message", "")} for r in csv.DictReader(f)]

    return {"files": files, "zip": "results.zip", "error": error, "errors": errors, "n_errors": len(errors), "n_contests": n_contests, "log": log.getvalue()}
