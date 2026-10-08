"""Local dev server for the web UI, with the optional native-Python backend.

    pip install -e .
    python web/build.py
    python web/serve.py            # http://localhost:8765

Serves web/ as static files. Also exposes the native backend the page can switch to when
it is loaded from localhost:

    GET  /api/health                 -> {"ok": true, "version": ...}
    POST /api/run                    multipart: contest_set_csv, run_config_json, files[]
    GET  /api/jobs/<id>/file?path=   one output file
    GET  /api/jobs/<id>/zip          results.zip

Both backends call runner.run_job, so the native path is the CLI code with no changes.
"""
import argparse
import email.parser
import email.policy
import functools
import importlib.metadata
import json
import pathlib
import tempfile
import urllib.parse
import uuid
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = pathlib.Path(__file__).resolve().parent
import sys  # noqa: E402

sys.path.insert(0, str(HERE))
import runner  # noqa: E402

JOBS_ROOT = pathlib.Path(tempfile.mkdtemp(prefix="rcv_cruncher_web_"))


def _safe_join(root: pathlib.Path, rel: str) -> pathlib.Path:
    p = (root / rel).resolve()
    if root.resolve() not in p.parents and p != root.resolve():
        raise ValueError("path escapes job directory")
    return p


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):  # quieter than the default
        if self.path.startswith("/api/"):
            super().log_message(fmt, *args)

    # ---- helpers
    def _json(self, status, obj):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _bytes(self, data: bytes, content_type="application/octet-stream", filename=None):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.end_headers()
        self.wfile.write(data)

    # ---- routes
    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path == "/api/health":
            try:
                version = importlib.metadata.version("rcv_cruncher")
            except importlib.metadata.PackageNotFoundError:
                version = "unknown"
            return self._json(200, {"ok": True, "version": version})
        if url.path.startswith("/api/jobs/"):
            parts = url.path.split("/")  # ['', 'api', 'jobs', id, 'file'|'zip']
            job_dir = JOBS_ROOT / parts[3]
            if not job_dir.is_dir():
                return self._json(404, {"error": "unknown job"})
            if parts[4] == "zip":
                return self._bytes((job_dir / "results.zip").read_bytes(), "application/zip", "results.zip")
            if parts[4] == "file":
                rel = urllib.parse.parse_qs(url.query).get("path", [""])[0]
                try:
                    p = _safe_join(job_dir, rel)
                    return self._bytes(p.read_bytes(), "text/plain; charset=utf-8")
                except (ValueError, FileNotFoundError):
                    return self._json(404, {"error": "no such file"})
            return self._json(404, {"error": "unknown route"})
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/run":
            return self._json(404, {"error": "unknown route"})
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        msg = email.parser.BytesParser(policy=email.policy.HTTP).parsebytes(
            b"Content-Type: " + self.headers["Content-Type"].encode() + b"\r\n\r\n" + body
        )
        fields, files = {}, []
        for part in msg.iter_parts():
            name = part.get_param("name", header="content-disposition")
            filename = part.get_filename()
            payload = part.get_payload(decode=True)
            if filename is not None:
                files.append((filename, payload))
            else:
                fields[name] = payload.decode("utf-8")

        job_id = uuid.uuid4().hex
        job_dir = JOBS_ROOT / job_id
        for rel, data in files:
            p = _safe_join(job_dir / "cvr", rel)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        result = runner.run_job(job_dir, fields.get("contest_set_csv", ""), fields.get("run_config_json", "{}"), capture_log=True)
        result["job_id"] = job_id
        return self._json(200, result)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    handler = functools.partial(Handler, directory=str(HERE))
    print(f"serving {HERE} at http://localhost:{args.port}  (jobs in {JOBS_ROOT})")
    ThreadingHTTPServer(("127.0.0.1", args.port), handler).serve_forever()


if __name__ == "__main__":
    main()
