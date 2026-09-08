#!/usr/bin/env python3
"""SploitAgent — Claude Code auto-capture hook (PostToolUse).

Claude Code runs this after every tool call and passes the call as JSON on
stdin. We record the meaningful *actions* (shell commands, web requests) into
the engagement's activity log automatically — so the console shows what the
agent did without the agent having to remember to log it. The agent still adds
the semantic layer on top (decisions, leads, findings, rationale).

Wiring (done for you by `sploit new`): a copy of this script lives at
<workspace>/.sploit/cc-activity-hook.py and <workspace>/.claude/settings.json
registers it as a PostToolUse hook. It writes activity.jsonl right next to
itself, so it needs no arguments and doesn't care about the cwd.

Design rules: never break Claude Code. Read stdin, best-effort append one or two
JSON lines, always exit 0, print nothing. Read-only toward everything but the log.
"""
import sys, os, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))          # <workspace>/.sploit
LOG  = os.path.join(HERE, "activity.jsonl")
MAXD = 300   # truncate long details / results

def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def clip(s, n=MAXD):
    s = " ".join(str(s).split())          # collapse whitespace to one line
    return s if len(s) <= n else s[:n-1] + "…"

def append(obj):
    obj["ts"] = now()
    obj["source"] = "hook"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj) + "\n")

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    name = data.get("tool_name", "") or ""
    ti   = data.get("tool_input", {}) or {}
    tr   = data.get("tool_response", data.get("tool_result", {}))

    # Only record the tools that represent a real action against the target.
    # Skip internal file/search tools (Read/Edit/Write/Grep/Glob/TodoWrite…) as noise.
    if name == "Bash":
        cmd = ti.get("command", "")
        if not cmd:
            return
        append({"event": "command", "tool": "Bash", "detail": clip(cmd, 500)})
        out = _result_text(tr)
        if out:
            append({"event": "result", "tool": "Bash", "detail": clip(out)})
    elif name in ("WebFetch", "WebSearch"):
        detail = ti.get("url") or ti.get("query") or ""
        if detail:
            append({"event": "command", "tool": name, "detail": clip(detail)})
    # else: ignore

def _result_text(tr):
    if tr is None:
        return ""
    if isinstance(tr, str):
        return tr.strip()
    if isinstance(tr, dict):
        for k in ("stdout", "output", "result", "content", "stderr"):
            v = tr.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
        return ""
    return ""

if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)   # never block a tool call
