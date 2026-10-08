// Web Worker hosting Pyodide. Messages in: {type:"init"} | {type:"run", job} | {type:"readFile", path}
// Messages out: {type:"boot", text} (runtime loading stage) | {type:"log", text} (python stdout/stderr) | {type:"ready", info} | {type:"result", ...} | {type:"file", path, data} | {type:"error", text}
let pyodide = null;
let meta = null;
const JOB_DIR = "/job";

const post = (msg) => self.postMessage(msg);
const log = (text) => post({ type: "log", text });
const boot = (text) => post({ type: "boot", text });

async function init() {
  meta = await (await fetch(new URL("dist/meta.json", self.location.href))).json();
  const base = `https://cdn.jsdelivr.net/pyodide/v${meta.pyodide_version}/full/`;
  boot(`pyodide ${meta.pyodide_version}`);
  const { loadPyodide } = await import(`${base}pyodide.mjs`);
  pyodide = await loadPyodide({ indexURL: base });
  // package-loader chatter goes to the runtime line, not the run log
  const quiet = { messageCallback: (t) => console.debug(t), errorCallback: boot };

  boot("pandas");
  await pyodide.loadPackage(["pandas", "tqdm", "micropip"], quiet);
  const wheelURL = new URL(`dist/${meta.wheel}`, self.location.href).href;
  boot(meta.wheel);
  await pyodide.runPythonAsync(`
import micropip
await micropip.install(["xmltodict", ${JSON.stringify(wheelURL)}])
`);
  // python stdout/stderr stream to the page log only from here on, so boot output never lands in a run's log
  pyodide.setStdout({ batched: log });
  pyodide.setStderr({ batched: log });
  const runnerSrc = await (await fetch(new URL("runner.py", self.location.href))).text();
  pyodide.FS.writeFile("/runner.py", runnerSrc);
  const info = pyodide.runPython(`
import sys, platform, pandas, importlib.metadata
sys.path.insert(0, "/")
import runner
f"python {platform.python_version()} · pandas {pandas.__version__} · rcv_cruncher {importlib.metadata.version('rcv_cruncher')}"
`);
  post({ type: "ready", info });
}

function resetJobDir() {
  const rm = (path) => {
    for (const name of pyodide.FS.readdir(path)) {
      if (name === "." || name === "..") continue;
      const full = `${path}/${name}`;
      if (pyodide.FS.isDir(pyodide.FS.stat(full).mode)) rm(full), pyodide.FS.rmdir(full);
      else pyodide.FS.unlink(full);
    }
  };
  if (pyodide.FS.analyzePath(JOB_DIR).exists) rm(JOB_DIR);
  else pyodide.FS.mkdir(JOB_DIR);
}

function writeFile(rel, data) {
  const parts = rel.split("/");
  let dir = JOB_DIR + "/cvr";
  if (!pyodide.FS.analyzePath(dir).exists) pyodide.FS.mkdir(dir);
  for (const p of parts.slice(0, -1)) {
    dir += "/" + p;
    if (!pyodide.FS.analyzePath(dir).exists) pyodide.FS.mkdir(dir);
  }
  pyodide.FS.writeFile(`${dir}/${parts[parts.length - 1]}`, new Uint8Array(data));
}

async function run(job) {
  resetJobDir();
  for (const f of job.files) writeFile(f.path, f.data);
  const result = pyodide.runPython(`
import json, runner
json.dumps(runner.run_job(${JSON.stringify(JOB_DIR)}, ${JSON.stringify(job.contest_set_csv)}, ${JSON.stringify(job.run_config_json)}))
`);
  post({ type: "result", ...JSON.parse(result) });
}

self.onmessage = async (e) => {
  const msg = e.data;
  try {
    if (msg.type === "init") await init();
    else if (msg.type === "run") await run(msg.job);
    else if (msg.type === "readFile") {
      const data = pyodide.FS.readFile(`${JOB_DIR}/${msg.path}`);
      post({ type: "file", path: msg.path, data }, [data.buffer]);
    }
  } catch (err) {
    post({ type: "error", text: String(err?.message ?? err) });
  }
};
