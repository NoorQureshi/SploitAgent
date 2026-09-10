#!/usr/bin/env python3
"""SploitAgent — Claude Code Stop hook that stops the agent giving up early.

The failure it fixes: the agent tries a couple of payloads on a feature, marks it
"not vulnerable", and pivots — instead of giving that lead the depth a real tester
would (fuzz every input, every context/encoding, blind/OOB variants).

Claude Code runs this when the agent tries to END its turn. It reads the engagement
activity log (next to this hook) and, if a lead was marked status:"failed" WITHOUT a
substantive coverage rationale, it BLOCKS the stop and tells the agent to go deeper
or honestly downgrade the lead to status:"open". It nudges once per stop cycle
(respects stop_hook_active) so it can never loop, only runs inside a sploit
workspace, and fails open on any error — it must never wedge a session.

Wiring (done by `sploit new`): a copy lives at <workspace>/.sploit/cc-thoroughness-hook.py
and <workspace>/.claude/settings.json registers it as a Stop hook.
"""
import sys, os, json

HERE = os.path.dirname(os.path.abspath(__file__))     # <workspace>/.sploit
LOG  = os.path.join(HERE, "activity.jsonl")
MIN_RATIONALE = 60   # a real "here's what I covered" note, not just "not vuln"

def load():
    out = []
    try:
        with open(LOG, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except ValueError:
                    pass
    except OSError:
        pass
    return out

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    # Already nudged in this stop cycle → let the agent finish (never loop).
    if data.get("stop_hook_active"):
        return 0

    weak = []
    for a in load():
        if str(a.get("status", "")).lower() == "failed":
            rat = (a.get("rationale") or "").strip()
            if len(rat) < MIN_RATIONALE:
                weak.append(a.get("lead") or (a.get("detail", "")[:40]) or "?")
    weak = sorted(set(weak))
    if not weak:
        return 0

    leads = ", ".join("`" + w + "`" for w in weak[:8])
    reason = (
        f"Not so fast — {len(weak)} lead(s) were marked status:\"failed\" without a coverage "
        f"rationale: {leads}. A real tester does not pivot after one or two payloads. For EACH "
        "of these, go deeper before you close it:\n"
        "  • fuzz every input — each parameter, plus headers, cookies, JSON fields, path segments\n"
        "  • work every context and every encoding / WAF-bypass variant\n"
        "  • try the blind / time-based / out-of-band variants when there's no visible response\n"
        "  • use the skill's cheatsheet.md as the checklist — run the set, not the first line\n"
        "Then EITHER record a `rationale` saying exactly what you covered (so 'failed' is trustworthy), "
        "OR downgrade the lead to status:\"open\" (you're not done — it isn't proven clean). "
        "Keep going; don't end the engagement with under-tested leads."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)   # fail open — never wedge the session
