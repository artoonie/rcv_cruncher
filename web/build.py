"""Build web/dist: a trimmed rcv_cruncher wheel plus meta.json for the page.

    python web/build.py

The wheel is built from the checkout with the bundled example data stripped out (it is
30 MB of CVRs the browser does not need). meta.json carries the option definitions so the
form renders before the Python runtime has loaded.
"""
import inspect
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
DIST = HERE / "dist"


def param_docs(func):
    """``{arg: text}`` from the ``:param arg:`` lines of a docstring (continuation lines are joined)."""
    docs, current = {}, None
    for line in (inspect.getdoc(func) or "").splitlines():
        m = re.match(r"\s*:param\s+(\w+):\s*(.*)", line)
        if m:
            current = m.group(1)
            docs[current] = m.group(2).strip()
        elif current and line.strip() and not line.strip().startswith(":"):
            docs[current] += " " + line.strip()
        else:
            current = None
    return docs


def main():
    sys.path.insert(0, str(ROOT / "src"))
    from rcv_cruncher.parsers import get_parser_dict  # noqa: E402
    from rcv_cruncher.rcv.variants import get_rcv_dict  # noqa: E402

    DIST.mkdir(exist_ok=True)
    for old in DIST.glob("*.whl"):
        old.unlink()

    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable, "-m", "pip", "wheel", str(ROOT), "--no-deps", "-w", tmp, "-q"], check=True)
        (src_wheel,) = pathlib.Path(tmp).glob("*.whl")
        dst_wheel = DIST / src_wheel.name
        with zipfile.ZipFile(src_wheel) as src, zipfile.ZipFile(dst_wheel, "w", zipfile.ZIP_DEFLATED) as dst:
            for item in src.infolist():
                if item.filename.startswith("rcv_cruncher/example/"):
                    continue
                dst.writestr(item, src.read(item))

    pkg = ROOT / "src" / "rcv_cruncher"
    pyodide_version = json.loads((ROOT / "tests" / "parity" / "package.json").read_text())["dependencies"]["pyodide"]
    meta = {
        "version": dst_wheel.name.split("-")[1],  # setup.py version; rcv_cruncher.__version__ is stale
        "wheel": dst_wheel.name,
        "pyodide_version": pyodide_version,
        "parsers": sorted(get_parser_dict().keys()),
        # extra arguments each parser takes beyond cvr_path, so the form can show one input per argument
        "parser_args": {
            name: [
                {"name": p.name, "required": p.default is inspect.Parameter.empty, "description": param_docs(f).get(p.name, "")}
                for p in inspect.signature(f).parameters.values()
                if p.name != "cvr_path"
            ]
            for name, f in get_parser_dict().items()
        },
        "rcv_types": sorted(get_rcv_dict().keys()),
        "contest_set_settings": json.loads((pkg / "contest_set_settings.json").read_text()),
        "run_config_settings": json.loads((pkg / "run_config_settings.json").read_text()),
    }
    (DIST / "meta.json").write_text(json.dumps(meta, indent=2))
    print(f"built {dst_wheel.relative_to(ROOT)} ({dst_wheel.stat().st_size // 1024} KB) and dist/meta.json")


if __name__ == "__main__":
    main()
