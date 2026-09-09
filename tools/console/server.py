#!/usr/bin/env python3
"""SploitAgent console — a tiny, read-only, local dashboard.

Shows what an agent is doing in an engagement (plan, live activity, findings) and
the skills library — by reading the workspace on disk, so it works with ANY agent
(Claude Code, OpenCode, Codex, Gemini, an API script). No dependencies, no writes,
no control over the agent. Binds to 127.0.0.1 only.

Run:  python3 tools/console/server.py [--port 8787] [--no-open]
Or:   sploit watch
"""
import argparse, glob, json, os, re, threading, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HOME = os.path.expanduser("~")
REG  = os.path.join(HOME, ".sploit", "engagements.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))          # tools/console/ -> repo root

def disp(path):
    """Shorten a workspace path for display (home → ~); the real path stays the key."""
    return "~" + path[len(HOME):] if path == HOME or path.startswith(HOME + os.sep) else path

def _read(path, limit=400000):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read(limit)
    except OSError:
        return ""

def registry():
    """Registered workspaces that still exist on disk (last entry per path wins)."""
    seen = {}
    for line in _read(REG).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except ValueError:
            continue
        p = o.get("path")
        if p:
            seen[p] = o
    return {p: o for p, o in seen.items() if os.path.isdir(p)}

def activity(path, tail=800):
    out = []
    for line in _read(os.path.join(path, ".sploit", "activity.jsonl")).splitlines()[-tail:]:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            out.append({"event": "note", "detail": line})
    return out

def findings(path):
    out = []
    for f in sorted(glob.glob(os.path.join(path, "findings", "*.md"))):
        base = os.path.basename(f)
        if base.startswith("_") or base.lower() in ("readme.md", "template.md"):
            continue                       # skip templates / readmes, not real findings
        txt = _read(f, 6000)
        m = re.search(r'^#\s+(.+)$', txt, re.M)
        title = m.group(1).strip() if m else os.path.basename(f)
        sev = ""
        # match "Severity: High", "**Severity:** High", "## Severity\nHigh", etc.
        s = re.search(r'(?im)^\s*[*_>#\s]*severity[*_:\s]+([A-Za-z]+)', txt)
        if s:
            sev = s.group(1).lower()
        out.append({"file": os.path.basename(f), "title": title, "severity": sev})
    return out

def summary(path, o):
    ev = activity(path)
    return {"target": o.get("target") or os.path.basename(path), "path": path, "disp": disp(path),
            "findings": len(findings(path)), "events": len(ev),
            "last": (ev[-1].get("ts") if ev else None), "created": o.get("ts")}

class H(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def _send(self, code, body, ctype="application/json"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body).encode()
        elif isinstance(body, str):
            body = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path in ("/", "/index.html"):
            return self._send(200, _read(os.path.join(HERE, "index.html")), "text/html; charset=utf-8")
        if u.path == "/api/engagements":
            reg = registry()
            items = sorted((summary(p, o) for p, o in reg.items()),
                           key=lambda x: (x["last"] or ""), reverse=True)
            return self._send(200, {"engagements": items})
        if u.path == "/api/engagement":
            path = (q.get("path") or [""])[0]
            if path not in registry():          # only registered, on-disk workspaces
                return self._send(404, {"error": "unknown engagement"})
            return self._send(200, {
                "target": os.path.basename(path),
                "path": path,
                "disp": disp(path),
                "scope": _read(os.path.join(path, "scope.txt"), 20000),
                "plan": _read(os.path.join(path, "plan.md"), 60000),
                "notes": _read(os.path.join(path, "notes.md"), 120000),
                "activity": activity(path),
                "findings": findings(path),
            })
        if u.path == "/api/finding":
            path = (q.get("path") or [""])[0]
            name = os.path.basename((q.get("file") or [""])[0])
            if path in registry() and name.endswith(".md"):
                return self._send(200, {"markdown": _read(os.path.join(path, "findings", name), 60000)})
            return self._send(404, {"error": "not found"})
        if u.path == "/api/skills":
            return self._send(200, _read(os.path.join(REPO, "docs", "skills.json")) or '{"skills":[]}')
        return self._send(404, {"error": "not found"})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), H)
    url = f"http://127.0.0.1:{a.port}"
    print(f"SploitAgent console → {url}   (read-only · local · Ctrl-C to stop)")
    if not a.no_open:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")

if __name__ == "__main__":
    main()
