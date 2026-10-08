# Native vs Pyodide parity check

The web UI runs `rcv_cruncher` in the browser with [Pyodide](https://pyodide.org) (CPython compiled
to WebAssembly). This directory proves that doing so produces byte-identical output to running the
CLI natively.

`contest_set/` is a batch-mode contest set that covers the tabulation variants (`SingleWinner`,
`Sequential`, `Until2`, `STVWholeBallot`, `STVFractionalBallot`), split stats, and every output
table, using the Minneapolis 2017 CVRs bundled in `src/rcv_cruncher/example`.

```sh
# native
python tests/parity/run_batch.py . tests/parity/out_native

# Pyodide (Node 20+; installs the pinned pyodide package)
(cd tests/parity && npm ci)
node tests/parity/run_pyodide.mjs tests/parity/out_pyodide

# diff
python tests/parity/compare.py tests/parity/out_native tests/parity/out_pyodide
```

`run_batch.py` is the *same* script in both cases; `run_pyodide.mjs` only mounts the repository
into Pyodide's filesystem and executes it. `compare.py` ignores files that only echo
run-specific inputs (timestamps, absolute paths).

`.github/workflows/parity.yml` runs this on every push. The Pyodide version is pinned in
`package.json`; bump it deliberately, since it also pins the pandas and numpy versions the web UI
will ship with.
