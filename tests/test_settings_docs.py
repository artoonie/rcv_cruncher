"""The settings JSON files are the single source of truth for option docs; keep the generated rst current."""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PKG = ROOT / "src" / "rcv_cruncher"


def test_generated_option_docs_are_current():
    result = subprocess.run([sys.executable, str(ROOT / "docs" / "gen_options.py"), "--check"], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout


def test_every_option_has_description_and_group():
    for fname in ("contest_set_settings.json", "run_config_settings.json"):
        settings = json.loads((PKG / fname).read_text())
        for name, spec in settings.items():
            assert spec.get("description"), f"{fname}: {name} has no description"
            assert spec.get("group"), f"{fname}: {name} has no group"
            for field in spec.get("applies_when", {}):
                assert field in settings, f"{fname}: {name} applies_when refers to unknown option {field}"
