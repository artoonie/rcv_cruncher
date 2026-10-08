"""Run the rcv_cruncher batch pipeline on the parity contest set.

Usage: python run_batch.py <repo_root> <output_dir>

The same script is executed under native CPython and under Pyodide (see run_pyodide.mjs),
so that compare.py can check the two environments produce byte-identical results.
"""
import json
import pathlib
import shutil
import sys
import warnings

warnings.simplefilter("ignore")

repo_root = pathlib.Path(sys.argv[1]).resolve()
output_dir = pathlib.Path(sys.argv[2]).resolve()

sys.path.insert(0, str(repo_root / "src"))

# batch mode writes its results next to the contest set, so work on a fresh copy.
# Clear the directory's contents rather than removing it: under Pyodide it is a mount point.
output_dir.mkdir(parents=True, exist_ok=True)
for child in output_dir.iterdir():
    shutil.rmtree(child) if child.is_dir() else child.unlink()
shutil.copytree(repo_root / "tests" / "parity" / "contest_set", output_dir, dirs_exist_ok=True)

run_config_path = output_dir / "run_config.json"
run_config = json.loads(run_config_path.read_text())
run_config["cvr_path_root"] = str(repo_root / "src" / "rcv_cruncher" / "example" / "example_cvr" / "minneapolis2017")
run_config_path.write_text(json.dumps(run_config, indent=4))

import rcv_cruncher.cli as cli  # noqa: E402

sys.argv = ["rcv-cruncher", str(output_dir), "--fresh"]
sys.exit(cli.main())
