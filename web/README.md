# rcv_cruncher web UI

Static page that runs the CLI's batch pipeline in the browser via Pyodide. Same code, same
outputs (enforced by `tests/parity`).

## Run locally

```sh
pip install -e .
python web/build.py     # -> web/dist/ (trimmed wheel + meta.json)
python web/serve.py     # http://localhost:8765
```

`serve.py` also provides a native-Python backend. When the page is served from localhost
and `/api/health` answers, a `backend: wasm · native` switch appears in the footer. It is
remembered per browser. On GitHub Pages only wasm exists.

## Deploy

`.github/workflows/pages.yml` builds `web/dist` and publishes `web/` with GitHub Pages.
Repository settings → Pages → Source must be set to "GitHub Actions" once.

## What the page exposes vs the CLI

The form is generated from `contest_set_settings.json` and `run_config_settings.json`, so
new options show up without touching the page. Besides `type`/`default` (which the CLI reads),
the page uses `group`, `description` (tooltip), `required`, `applies_when` (conditional
display), `placeholder`, `wide` (full-width field), `web_default` (the form's starting value
where it differs from the CLI default; the form writes every value explicitly, so the CLI
sees the same thing) and `deprecated` (hidden).

Page-only settings live at the top of `app.js`: which groups are open, the exhaust-rule presets
offered in Ballot rules, and the "Tabulation Rules from Previous Elections" link URL. Deliberately not
exposed:

| CLI option | Why |
|---|---|
| `contest_set_path` positional | replaced by the form; `Import contest_set.csv` loads an existing file into it |
| `--fresh` | every run is fresh |
| `--output_path` | the CLI ignores it (output always goes next to the contest set) |
| `cvr_path_root` (run_config) | replaced by file upload |
| `cvr_path` column | replaced by the per-contest file picker; the CSV value is shown as a hint after import |
| `ignore_contest` column | remove the contest instead |
| `ballot_stats_debug`, `cvr_ballot_allocation_rank_format`, `cvr_ballot_allocation_candidate_format` | dead flags: their steps are commented out in `batch.py` |

`extra_parser_args` is shown as one input per argument of the selected parser (names,
required flags and tooltips come from the parser signatures and `:param` docstrings via
`build.py`); it is still stored and exported as the CLI's `k=v;k2=v2` string. The raw string
is shown when no parser is selected or the string holds keys the parser does not declare.

Parsers offered are exactly the CLI's registry (`get_parser_dict`). Functions in
`parsers.py` that are not registered (`candidate_column_csv2`, `dominion5_10_Alaska2024`,
`santafe`, `hart_redondo_beach`) are unavailable in both.

Directory-based parsers (`dominion5_10`, `choice_pro_plus`, `ess1`, `ess2`, `unisyn`) take a
folder: use the Folder button next to the file picker.

## Files

- `index.html`, `app.js`: the page. No build step, no dependencies.
- `worker.js`: Web Worker that loads Pyodide from jsdelivr (version pinned in `tests/parity/package.json`), installs the wheel, runs jobs.
- `runner.py`: runs one job directory through `batch.py` and zips the outputs. Used by both the worker and `serve.py`.
- `build.py`: builds `dist/`.
- `serve.py`: dev server + native backend (stdlib only).
