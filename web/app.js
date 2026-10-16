"use strict";
// Columns of contest_set.csv the web UI does not expose (see web/README.md).
const SKIP_COLUMNS = new Set(["ignore_contest"]);
// Columns that the CLI reads as "no value" when the cell is empty.
const EMPTY_DEFAULTS = new Set(["", "None", "np.nan"]);
// Groups shown expanded by default; the rest collapse to a summary of non-default values.
const OPEN_GROUPS = new Set(["Election", "Input", "Tabulation", "Ballot rules"]);
// Link shown top right. Leave empty to hide the button.
const TABULATION_RULES_URL = "https://docs.google.com/spreadsheets/d/1JKTHia4iSNT16dhEOmsEtS0muisUgT3_1WD3PvIAoBU";
// Presets for the three exhaust rules, offered in the Ballot rules group. The first is the page default.
const EXHAUST_PRESETS = [
  { name: "MN", values: { exhaust_on_overvote_marks: false, exhaust_on_duplicate_candidate_marks: false, exhaust_on_N_repeated_skipped_marks: "0" } },
  { name: "CA/NM/NYC", values: { exhaust_on_overvote_marks: true, exhaust_on_duplicate_candidate_marks: false, exhaust_on_N_repeated_skipped_marks: "0" } },
  { name: "AK/DC/ME", values: { exhaust_on_overvote_marks: true, exhaust_on_duplicate_candidate_marks: false, exhaust_on_N_repeated_skipped_marks: "2" } },
  { name: "Strict", values: { exhaust_on_overvote_marks: true, exhaust_on_duplicate_candidate_marks: true, exhaust_on_N_repeated_skipped_marks: "1" } },
];
const PRESETS_FOR_GROUP = { "Ballot rules": EXHAUST_PRESETS };
const ACRONYMS = { rcv: "RCV", cvr: "CVR", json: "JSON", csv: "CSV", stv: "STV", n: "N", fvdbfmt: "FvDB Format", id: "ID" };

const $ = (id) => document.getElementById(id);
const el = (tag, attrs = {}, ...children) => {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") n.className = v;
    else if (k.startsWith("on")) n.addEventListener(k.slice(2), v);
    else if (v !== undefined && v !== null && v !== false) n.setAttribute(k, v === true ? "" : v);
  }
  for (const c of children) n.append(c);
  return n;
};
// snake_case -> Title Case, keeping known acronyms: per_rcv_group_stats_fvDBfmt -> "Per RCV Group Stats FvDB Format"
const titleCase = (key) => key.split("_").filter(Boolean).map((w) => ACRONYMS[w.toLowerCase()] ?? w[0].toUpperCase() + w.slice(1)).join(" ");

let meta = null;
let contests = []; // [{values:{col:string|boolean}, files:File[]}]
let backend = "wasm";
let worker = null;
let workerReady = false;
let lastJob = null; // {backend, job_id?, files}

// ---------------------------------------------------------------- option helpers
const columns = () => Object.entries(meta.contest_set_settings).filter(([c]) => !SKIP_COLUMNS.has(c));
const groupsOf = (entries) => {
  const g = new Map();
  for (const [name, spec] of entries) (g.get(spec.group) ?? g.set(spec.group, []).get(spec.group)).push([name, spec]);
  return g;
};
const defaultOf = (spec) => {
  const d = spec.web_default ?? spec.default;
  return spec.type === "bool" ? d === true : EMPTY_DEFAULTS.has(String(d)) ? "" : String(d);
};
const isDefault = (spec, v) => v === defaultOf(spec) || (v === "" && EMPTY_DEFAULTS.has(String(spec.default)));
// applies_when: {field: [allowed values]}; a field is applicable when every condition holds
const applies = (spec, values) => Object.entries(spec.applies_when ?? {}).every(([f, allowed]) => allowed.includes(values[f]));
const fmtValue = (spec, v) => (spec.type === "bool" ? (v ? "on" : "off") : String(v));

// extra_parser_args is stored as the CLI's "k=v;k2=v2" string; these mirror batch._cast_dict
const parseArgs = (text) => {
  const d = {};
  for (const part of (text || "").split(";")) {
    if (!part.trim()) continue;
    const i = part.indexOf("=");
    if (i < 0) d[part] = "";
    else d[part.slice(0, i)] = part.slice(i + 1).trim();
  }
  return d;
};
const formatArgs = (d) => Object.entries(d).filter(([, v]) => v !== "").map(([k, v]) => `${k}=${v}`).join(";");

// one input per argument of the selected parser; returns a list of field elements
function parserArgFields(spec, contest, refresh) {
  const parser = contest.values.parser_func;
  const args = meta.parser_args[parser] ?? [];
  const current = parseArgs(contest.values.extra_parser_args);
  const known = new Set(args.map((a) => a.name));
  const unknown = Object.keys(current).filter((k) => !known.has(k));
  const set = (name, v) => { current[name] = v; contest.values.extra_parser_args = formatArgs(current); refresh(); };
  const fields = args.map((a) => {
    const input = el("input", { type: "text", value: current[a.name] ?? "" });
    input.addEventListener("input", () => set(a.name, input.value));
    return el("div", { class: "field" }, el("label", { title: a.description || `${a.name} argument of ${parser}` }, titleCase(a.name), ...(a.required ? [el("span", { class: "req" }, "*")] : [])), input);
  });
  // no parser yet, or keys the parser does not declare: show the raw string so nothing is hidden or lost
  if (!parser || unknown.length) {
    const input = el("input", { type: "text", value: contest.values.extra_parser_args ?? "", placeholder: "k=v;k2=v2" });
    input.addEventListener("input", () => { contest.values.extra_parser_args = input.value; refresh(); });
    fields.push(el("div", { class: "field" },
      el("label", { title: spec.description }, titleCase("extra_parser_args")), input,
      unknown.length ? el("div", { class: "hint" }, `${parser} does not take: ${unknown.join(", ")}`) : ""));
  }
  return fields;
}

// ---------------------------------------------------------------- contests form
function fieldWidget(col, spec, contest, idx, rerender, refresh) {
  if (col === "extra_parser_args") return parserArgFields(spec, contest, refresh);
  const value = contest.values[col];
  const text = (c) => (spec.required ? [titleCase(c), el("span", { class: "req" }, "*")] : [titleCase(c)]);
  const label = el("label", { title: spec.description }, ...text(col));
  if (col === "cvr_path") {
    // A recreated <input type=file> cannot carry its selection, so the input is hidden and the
    // selection is shown in text next to a button that opens the picker.
    const input = el("input", { type: "file", multiple: true, class: "hidden" });
    input.addEventListener("change", () => { contest.files = [...input.files]; rerender(); });
    const pick = el("button", { type: "button", onclick: () => { input.removeAttribute("webkitdirectory"); input.click(); } }, contest.files.length ? "Change" : "Choose file");
    const folder = el("button", { type: "button", title: "Select a folder, for parsers that read a directory", onclick: () => { input.setAttribute("webkitdirectory", ""); input.click(); } }, "Folder");
    let chosen = "";
    if (contest.files.length === 1) chosen = contest.files[0].webkitRelativePath ? contest.files[0].webkitRelativePath.split("/")[0] + "/" : contest.files[0].name;
    else if (contest.files.length > 1) chosen = `${contest.files.length} files` + (contest.files[0].webkitRelativePath ? ` in ${contest.files[0].webkitRelativePath.split("/")[0]}/` : "");
    const expected = contest.values.cvr_path ? `contest_set.csv: ${contest.values.cvr_path}` : "";
    return el("div", { class: `field files${spec.wide ? " wide" : ""}` },
      el("label", { title: spec.description }, ...text(col)),
      el("div", { class: "filerow" }, pick, folder, el("span", { class: chosen ? "chosen" : "hint" }, chosen || "none selected")),
      ...(chosen || !expected ? [] : [el("div", { class: "hint" }, expected)]), input);
  }
  if (spec.type === "bool") {
    const input = el("input", { type: "checkbox", id: `c${idx}-${col}` });
    input.checked = value === true;
    input.addEventListener("change", () => { contest.values[col] = input.checked; rerender(); });
    return el("div", { class: `field bool${spec.wide ? " wide" : ""}` }, input, el("label", { for: `c${idx}-${col}`, title: spec.description }, titleCase(col)));
  }
  if (spec.type === "func") {
    const options = col === "rcv_type" ? meta.rcv_types : meta.parsers;
    const select = el("select", {}, el("option", { value: "", disabled: true }, "—"), ...options.map((o) => el("option", { value: o }, o)));
    select.value = value || "";
    select.addEventListener("change", () => { contest.values[col] = select.value; rerender(); });
    return el("div", { class: `field${spec.wide ? " wide" : ""}` }, label, select);
  }
  const placeholder = spec.placeholder ?? (spec.type === "list" ? "a,b" : spec.type === "dict" ? "k=v;k2=v2" : "");
  const input = el("input", { type: "text", value: value ?? "", placeholder });
  // text edits never change which fields apply, so update the title and group summaries in place
  input.addEventListener("input", () => { contest.values[col] = input.value; refresh(); });
  return el("div", { class: `field${spec.wide ? " wide" : ""}` }, label, input);
}

function newContest(values = {}) {
  const v = {};
  for (const [col, spec] of columns()) v[col] = defaultOf(spec);
  return { values: { ...v, ...values }, files: [] };
}

function contestTitle(c, idx) {
  const parts = [c.values.jurisdiction, c.values.office, c.values.year].filter(Boolean);
  return parts.length ? parts.join(" · ") : `Contest ${idx + 1}`;
}

function summaryNodes(group, entries, c, rerender) {
  const visible = entries.filter(([, spec]) => applies(spec, c.values));
  const changed = visible.filter(([col, spec]) => !isDefault(spec, c.values[col])).map(([col, spec]) => `${titleCase(col)}: ${fmtValue(spec, c.values[col])}`);
  const reset = el("button", { type: "button", class: "small", onclick: (e) => { e.stopPropagation(); for (const [col, spec] of entries) c.values[col] = defaultOf(spec); rerender(); } }, "reset");
  return [el("span", { class: "group-title" }, group),
    ...(changed.length ? [el("span", { class: "summary-values", title: changed.join(", ") }, changed.join(", ")), reset] : [el("span", { class: "pill" }, "defaults")])];
}

function renderContest(idx) {
  const c = contests[idx];
  const card = el("div", { class: "contest" });
  const groups = groupsOf(columns());
  const refresh = () => {
    card.querySelector(".head b").textContent = contestTitle(c, idx);
    for (const d of card.querySelectorAll("details.group")) d.querySelector("summary").replaceChildren(...summaryNodes(d.dataset.group, groups.get(d.dataset.group), c, rerender));
  };
  const rerender = () => {
    // remember which collapsible groups are open (read from the DOM: the toggle event can fire after a re-render)
    c.open = new Set([...card.querySelectorAll("details.group[open]")].map((d) => d.dataset.group));
    card.replaceWith(renderContest(idx));
  };
  card.append(el("div", { class: "head" },
    el("b", {}, contestTitle(c, idx)),
    el("span", {},
      el("button", { onclick: () => { contests.splice(idx + 1, 0, { values: { ...c.values }, files: [] }); renderContests(); } }, "Duplicate"), " ",
      el("button", { disabled: contests.length === 1, onclick: () => { if (c.files.length && !confirm(`Remove ${contestTitle(c, idx)}?`)) return; contests.splice(idx, 1); renderContests(); } }, "Remove"))));

  for (const [group, entries] of groups) {
    const visible = entries.filter(([, spec]) => applies(spec, c.values));
    const grid = el("div", { class: "grid" }, ...visible.flatMap(([col, spec]) => fieldWidget(col, spec, c, idx, rerender, refresh)));
    if (OPEN_GROUPS.has(group)) {
      const presets = PRESETS_FOR_GROUP[group];
      const row = presets ? el("div", { class: "presets" }, "Preset:", ...presets.map((p) => {
        const active = Object.entries(p.values).every(([k, v]) => c.values[k] === v);
        return el("button", { type: "button", class: `small${active ? " on" : ""}`, onclick: () => { Object.assign(c.values, p.values); rerender(); } }, p.name);
      })) : "";
      card.append(el("div", { class: "group" }, el("div", { class: "group-title" }, group), row, grid));
      continue;
    }
    const details = el("details", { class: "group", "data-group": group, open: c.open?.has(group) },
      el("summary", {}, ...summaryNodes(group, entries, c, rerender)),
      grid);
    card.append(details);
  }
  return card;
}

function renderContests() {
  $("contests").replaceChildren(...contests.map((_, idx) => renderContest(idx)));
}

// cvr_path written to contest_set.csv, relative to the job's cvr/ root
function cvrPathFor(c, idx) {
  if (!c.files.length) return c.values.cvr_path || ""; // keep the imported value so an export still works with the CLI
  if (c.files.length === 1 && !c.files[0].webkitRelativePath) return `${idx}/${c.files[0].name}`;
  return `${idx}`;
}
// path of each uploaded file under cvr/
function filePathsFor(c, idx) {
  return c.files.map((f) => {
    const rel = f.webkitRelativePath ? f.webkitRelativePath.split("/").slice(1).join("/") : f.name;
    return { file: f, path: `${idx}/${rel}` };
  });
}

// Read every file's bytes with bounded concurrency and retries: launching tens of thousands of
// concurrent reads at once makes Chromium fail random ones with NotReadableError.
async function readAll(files, concurrency = 64) {
  const out = new Array(files.length);
  let next = 0, done = 0;
  const readOne = async (f, attempt = 0) => {
    try { return await f.file.arrayBuffer(); }
    catch (err) {
      if (attempt >= 4) throw new Error(`Cannot read ${f.file.webkitRelativePath || f.file.name}: ${err.message ?? err} — the file may have changed since selection, be online-only in a cloud drive, or lack read permission; re-select the folder and retry`);
      await new Promise((r) => setTimeout(r, 100 * 2 ** attempt));
      return readOne(f, attempt + 1);
    }
  };
  await Promise.all(Array.from({ length: Math.min(concurrency, files.length) }, async () => {
    while (next < files.length) {
      const i = next++;
      out[i] = { path: files[i].path, data: await readOne(files[i]) };
      if (runState) runState.progress = `reading files ${++done}/${files.length}`;
    }
  }));
  if (runState) runState.progress = "";
  return out;
}

// ---------------------------------------------------------------- csv
const csvCell = (v) => {
  const s = v === true ? "TRUE" : v === false ? "FALSE" : String(v ?? "");
  return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
};
function contestSetCsv() {
  const cols = columns().map(([c]) => c);
  const rows = contests.map((c, idx) => cols.map((col) => csvCell(col === "cvr_path" ? cvrPathFor(c, idx) : c.values[col])).join(","));
  return [cols.join(","), ...rows].join("\n") + "\n";
}
function parseCsv(text) {
  const rows = [];
  let row = [], cell = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (q) {
      if (ch === '"' && text[i + 1] === '"') { cell += '"'; i++; }
      else if (ch === '"') q = false;
      else cell += ch;
    } else if (ch === '"') q = true;
    else if (ch === ",") { row.push(cell); cell = ""; }
    else if (ch === "\n" || ch === "\r") { if (ch === "\r" && text[i + 1] === "\n") i++; row.push(cell); rows.push(row); row = []; cell = ""; }
    else cell += ch;
  }
  if (cell !== "" || row.length) { row.push(cell); rows.push(row); }
  return rows.filter((r) => r.some((c) => c !== ""));
}
function importCsv(text) {
  const [header, ...rows] = parseCsv(text.replace(/^﻿/, ""));
  const unknown = header.filter((h) => !(h in meta.contest_set_settings));
  contests = rows.map((r) => {
    const values = {};
    header.forEach((h, i) => {
      const spec = meta.contest_set_settings[h];
      if (!spec || SKIP_COLUMNS.has(h)) return;
      const raw = r[i] ?? "";
      values[h] = spec.type === "bool" ? (raw === "" ? spec.default === true : raw.trim().toLowerCase() === "true") : raw;
    });
    return newContest(values);
  });
  renderContests();
  setStatus(unknown.length ? `Imported ${rows.length} contest(s); ignored unknown column(s): ${unknown.join(", ")}` : `Imported ${rows.length} contest(s). Pick the CVR file for each.`);
}

// ---------------------------------------------------------------- outputs
function renderOutputs() {
  const root = $("outputs");
  const entries = Object.entries(meta.run_config_settings).filter(([k, spec]) => k !== "cvr_path_root" && !spec.deprecated);
  for (const [group, items] of groupsOf(entries)) {
    const box = el("div", { class: "outgroup" }, el("div", { class: "group-title" }, group));
    for (const [key, spec] of items) {
      const input = el("input", { type: "checkbox", id: `out-${key}` });
      input.checked = (spec.web_default ?? spec.default) === true;
      box.append(el("label", { title: spec.description }, input, titleCase(key)));
    }
    root.append(box);
  }
  $("outAll").onclick = () => root.querySelectorAll("input").forEach((i) => (i.checked = true));
  $("outNone").onclick = () => root.querySelectorAll("input").forEach((i) => (i.checked = false));
}
function runConfigJson() {
  const cfg = {};
  for (const [key, spec] of Object.entries(meta.run_config_settings)) {
    if (key === "cvr_path_root" || spec.deprecated) continue;
    cfg[key] = $(`out-${key}`).checked;
  }
  return JSON.stringify(cfg, null, 2);
}

// ---------------------------------------------------------------- backends
function setStatus(text, state = "") { $("status").textContent = text; $("status").className = state === true ? "err" : state || ""; }
const ANSI = /\x1b\[[0-9;]*m/g;
const PROGRESS = /(\d+) of (\d+) contests: (.*?):\s*\d+%\|/;
let runState = null; // {start, timer, progress}
// backend name for status text, only when the user can switch backends (localhost); "" on the public site
const where = (sep = " · ") => ($("backendSwitch").classList.contains("hidden") ? "" : `${backend}${sep}`);
const elapsed = () => `${((performance.now() - runState.start) / 1000).toFixed(1)} s`;
function tickStatus() {
  if (!runState) return;
  setStatus(`Running · ${where()}${runState.progress ? `${runState.progress} · ` : ""}${elapsed()}`);
}
function appendLog(text) {
  // tqdm redraws its bar with \r; keep only the final redraw of each line
  const clean = text.replace(ANSI, "").split("\n").map((line) => line.slice(line.lastIndexOf("\r") + 1)).join("\n");
  const l = $("log"); l.textContent += clean + "\n"; l.scrollTop = l.scrollHeight;
  if (runState) {
    const m = clean.match(PROGRESS);
    if (m) { runState.progress = `${m[1]}/${m[2]}: ${m[3].trim()}`; tickStatus(); }
  }
}
function endRun() { if (runState) clearInterval(runState.timer); const t = runState ? elapsed() : ""; runState = null; return t; }
function setLogVisible(show) { $("log").classList.toggle("hidden", !show); $("logToggle").textContent = show ? "Hide log" : "Show log"; }

function startWorker() {
  if (worker) return;
  worker = new Worker("worker.js", { type: "module" });
  worker.onmessage = (e) => {
    const m = e.data;
    if (m.type === "log") { if (workerReady) appendLog(m.text); else console.debug("[pyodide boot]", m.text); }
    else if (m.type === "boot") { $("runtime").textContent = `loading ${m.text} …`; if (backend === "wasm" && !workerReady) setStatus(`Loading python runtime · ${m.text} …`); }
    else if (m.type === "ready") { workerReady = true; $("runtime").textContent = m.info; if (backend === "wasm") { setStatus(`Ready${where() ? " · wasm" : ""}`); $("run").disabled = false; } }
    else if (m.type === "result") finishRun(m);
    else if (m.type === "file" && m.path !== "results.zip") showPreview(m.path, new TextDecoder().decode(m.data));
    else if (m.type === "error") { endRun(); setStatus(m.text, true); appendLog(m.text); setLogVisible(true); $("run").disabled = !(workerReady || backend === "native"); }
  };
  worker.postMessage({ type: "init" });
}

async function runNative(job) {
  const fd = new FormData();
  fd.append("contest_set_csv", job.contest_set_csv);
  fd.append("run_config_json", job.run_config_json);
  for (const f of job.files) fd.append("files[]", f.file, f.path);
  const r = await fetch("/api/run", { method: "POST", body: fd });
  if (!r.ok) throw new Error(`native backend: HTTP ${r.status}`);
  finishRun(await r.json());
}

async function run() {
  if (!contests.length) return setStatus("Add a contest first", true);
  const missing = contests.map((c, i) => {
    const names = columns().filter(([col, spec]) => spec.required && (col === "cvr_path" ? !c.files.length : !c.values[col])).map(([col]) => titleCase(col));
    const given = parseArgs(c.values.extra_parser_args);
    for (const a of meta.parser_args[c.values.parser_func] ?? []) if (a.required && !given[a.name]) names.push(titleCase(a.name));
    return names.length ? `${contestTitle(c, i)}: missing ${names.join(", ")}` : null;
  }).filter(Boolean);
  if (missing.length) return setStatus(missing.join("; "), true);
  $("run").disabled = true;
  $("log").textContent = "";
  appendLog(`── ${backend} · ${new Date().toLocaleTimeString()} ──`);
  $("logSection").classList.remove("hidden");
  $("resultsSection").classList.add("hidden");
  runState = { start: performance.now(), timer: setInterval(tickStatus, 1000), progress: "" };
  tickStatus();
  const files = contests.flatMap((c, idx) => filePathsFor(c, idx));
  const job = { contest_set_csv: contestSetCsv(), run_config_json: runConfigJson(), files };
  try {
    if (backend === "native") await runNative(job);
    else {
      const payload = { ...job, files: await readAll(files) };
      worker.postMessage({ type: "run", job: payload }, payload.files.map((f) => f.data));
    }
  } catch (err) {
    endRun();
    setStatus(String(err.message ?? err), true);
    $("run").disabled = false;
  }
}

function finishRun(result) {
  const took = endRun();
  if (result.log) appendLog(result.log.trimEnd());
  $("run").disabled = false;
  lastJob = { backend, job_id: result.job_id, files: result.files };
  const n = result.n_contests ?? contests.length;
  const plural = (k, w) => `${k} ${w}${k === 1 ? "" : "s"}`;
  if (result.error) {
    setStatus(`Failed · ${where()}${took} · see log`, true);
    appendLog(result.error);
    setLogVisible(true);
    $("logSection").scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }
  renderFiles(result.files);
  $("resultsSection").classList.remove("hidden");
  if (result.n_errors) {
    // the first failed step per contest is the cause; later steps fail because the contest object is missing
    const seen = new Set();
    for (const e of result.errors ?? []) if (!seen.has(e.contest)) { seen.add(e.contest); appendLog(`ERROR ${e.contest} · ${e.step}: ${e.message}`); }
    setLogVisible(true);
    setStatus(`Done · ${where()}${seen.size} of ${plural(n, "contest")} failed · ${plural(result.files.length, "file")} · ${took} · see log and results/error_log.csv`, true);
    const li = [...$("files").querySelectorAll("li:not(.dir)")].find((x) => x.dataset.path === "results/error_log.csv");
    if (li) li.click();
  } else {
    setStatus(`Done · ${where()}${plural(n, "contest")} · ${plural(result.files.length, "file")} · ${took}`, "ok");
  }
  $("runBar").scrollIntoView({ behavior: "smooth", block: "start" });
}

// ---------------------------------------------------------------- results
function renderFiles(files) {
  const ul = $("files");
  ul.replaceChildren();
  $("preview").replaceChildren();
  let lastDir = null;
  const dirOf = (p) => p.split("/").slice(0, -1).join("/");
  const rank = (p) => (p.startsWith("results") ? 0 : 1);
  files = [...files].sort((a, b) => rank(a.path) - rank(b.path) || dirOf(a.path).localeCompare(dirOf(b.path)) || a.path.localeCompare(b.path));
  $("fileCount").textContent = `${files.length} files`;
  for (const f of files) {
    const dir = dirOf(f.path);
    if (dir !== lastDir) { ul.append(el("li", { class: "dir" }, dir)); lastDir = dir; }
    const li = el("li", { "data-path": f.path, title: f.path, onclick: () => { ul.querySelectorAll("li.sel").forEach((x) => x.classList.remove("sel")); li.classList.add("sel"); openFile(f.path); } },
      el("span", {}, f.path.split("/").pop()), el("span", { class: "sz" }, fmtSize(f.size)));
    ul.append(li);
  }
}
const fmtSize = (n) => (n < 1024 ? `${n} B` : n < 1048576 ? `${(n / 1024).toFixed(0)} KB` : `${(n / 1048576).toFixed(1)} MB`);

async function openFile(path) {
  if (lastJob.backend === "native") {
    const r = await fetch(`/api/jobs/${lastJob.job_id}/file?path=${encodeURIComponent(path)}`);
    showPreview(path, await r.text());
  } else worker.postMessage({ type: "readFile", path });
}

function showPreview(path, text) {
  const root = $("preview");
  root.replaceChildren();
  const name = path.split("/").pop();
  const blob = new Blob([text], { type: "text/plain" });
  root.append(el("div", { class: "preview-head" }, el("b", {}, path), el("a", { class: "btn small", href: URL.createObjectURL(blob), download: name }, "download")));
  const MAX = 500;
  if (path.endsWith(".csv")) {
    const rows = parseCsv(text);
    const table = el("table");
    const NUM = /^-?\d+(\.\d+)?%?$/;
    const body = rows.slice(1);
    const width = Math.max(...rows.map((r) => r.length));
    const numeric = Array.from({ length: width }, (_, j) => body.some((r) => (r[j] ?? "") !== "") && body.every((r) => (r[j] ?? "") === "" || NUM.test(r[j])));
    rows.slice(0, MAX).forEach((r, i) => table.append(el("tr", {}, ...r.map((c, j) => el(i === 0 ? "th" : "td", { class: numeric[j] ? "num" : undefined }, c)))));
    root.append(table);
    if (rows.length > MAX) root.append(el("div", { class: "preview-note" }, `… ${rows.length - MAX} more rows (download to see all)`));
  } else root.append(el("pre", {}, text.length > 200000 ? text.slice(0, 200000) + "\n… truncated" : text));
}

async function downloadZip() {
  if (!lastJob) return;
  if (lastJob.backend === "native") { window.location.href = `/api/jobs/${lastJob.job_id}/zip`; return; }
  const data = await new Promise((resolve) => {
    const h = (e) => { if (e.data.type === "file" && e.data.path === "results.zip") { worker.removeEventListener("message", h); resolve(e.data.data); } };
    worker.addEventListener("message", h);
    worker.postMessage({ type: "readFile", path: "results.zip" });
  });
  const a = el("a", { href: URL.createObjectURL(new Blob([data], { type: "application/zip" })), download: "results.zip" });
  document.body.append(a); a.click(); a.remove();
}

// ---------------------------------------------------------------- backend switch (local only)
async function setupBackendSwitch() {
  const local = ["localhost", "127.0.0.1"].includes(location.hostname);
  if (!local) return;
  let native = false;
  try { native = (await (await fetch("/api/health")).json()).ok === true; } catch { /* no server */ }
  if (!native) return;
  const sw = $("backendSwitch");
  sw.classList.remove("hidden");
  const apply = (b) => {
    backend = b;
    try { localStorage.setItem("rcv_backend", b); } catch { /* ignore */ }
    sw.querySelectorAll("a").forEach((a) => a.classList.toggle("on", a.dataset.b === b));
    if (b === "native") { setStatus("Ready · native"); $("run").disabled = false; }
    else { setStatus(workerReady ? "Ready · wasm" : "Loading python runtime …"); $("run").disabled = !workerReady; }
  };
  sw.querySelectorAll("a").forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); apply(a.dataset.b); }));
  let saved = "wasm";
  try { saved = localStorage.getItem("rcv_backend") || "wasm"; } catch { /* ignore */ }
  apply(saved);
}

// ---------------------------------------------------------------- boot
(async function main() {
  meta = await (await fetch("dist/meta.json")).json();
  $("version").textContent = meta.version;
  if (TABULATION_RULES_URL) { $("rulesLink").href = TABULATION_RULES_URL; $("rulesLink").classList.remove("hidden"); }
  renderOutputs();
  contests = [newContest()];
  renderContests();
  $("add").onclick = () => { contests.push(newContest()); renderContests(); };
  $("import").onclick = () => $("importFile").click();
  $("importFile").onchange = async () => { if ($("importFile").files[0]) importCsv(await $("importFile").files[0].text()); $("importFile").value = ""; };
  $("export").onclick = () => {
    const a = el("a", { href: URL.createObjectURL(new Blob([contestSetCsv()], { type: "text/csv" })), download: "contest_set.csv" });
    document.body.append(a); a.click(); a.remove();
  };
  $("run").onclick = run;
  $("zip").onclick = downloadZip;
  $("logToggle").onclick = () => setLogVisible($("log").classList.contains("hidden"));
  setStatus("Loading python runtime …");
  startWorker();
  await setupBackendSwitch();
})();
