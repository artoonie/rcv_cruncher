// Run tests/parity/run_batch.py inside Pyodide (WebAssembly CPython) under Node.
// Usage: node run_pyodide.mjs [output_dir]   (default: tests/parity/out_pyodide)
import { loadPyodide } from "pyodide";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(here, "..", "..");
const outputDir = path.resolve(process.argv[2] ?? path.join(here, "out_pyodide"));
fs.mkdirSync(outputDir, { recursive: true });

const pyodide = await loadPyodide();
await pyodide.loadPackage(["pandas", "tqdm", "micropip"]);
await pyodide.runPythonAsync(`import micropip; await micropip.install("xmltodict")`);

pyodide.FS.mkdir("/repo");
pyodide.mountNodeFS("/repo", repoRoot);
pyodide.FS.mkdir("/out");
pyodide.mountNodeFS("/out", outputDir);

console.log(pyodide.runPython(`
import sys, platform, pandas, numpy
f"pyodide: python {platform.python_version()} ({platform.system()}) pandas {pandas.__version__} numpy {numpy.__version__}"
`));

pyodide.runPython(`import sys; sys.argv = ["run_batch.py", "/repo", "/out"]`);
try {
  pyodide.runPython(fs.readFileSync(path.join(here, "run_batch.py"), "utf8"));
} catch (err) {
  // run_batch.py ends with sys.exit(); treat exit code 0 as success
  if (!(err?.type === "SystemExit" && /^SystemExit: (0|None)?$/.test(err.message.trim().split("\n").pop()))) {
    throw err;
  }
}
console.log(`pyodide run complete: ${outputDir}`);
