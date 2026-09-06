---
name: code-review-python
description: >
  Security review of Python code — dangerous sinks and framework-specific pitfalls (Django/Flask/
  FastAPI). Load when reviewing a Python codebase/PR, on .py source in scope, or "review this Python".
  Signals: requirements.txt/pyproject, Django/Flask/FastAPI, ORMs, pickle/yaml, subprocess.
domain: code-review
type: reference
stability: learning
modes: [bugbounty, defense, pentest]
severity: info
cwe: [CWE-94, CWE-89, CWE-78, CWE-502]
tools: [semgrep, bandit, ripgrep]
schema_version: 1
---

# Python security code review

## When it applies
You're reading Python source (a repo, a PR, a service). This is the language-specific companion to
`code-review-methodology` — the exact sinks and framework gotchas to grep and trace.

## Why it works
Most severe Python bugs come from a known set of sinks plus framework misuse. Grep the sinks, trace
each argument to a user source, and check the framework's safe-vs-unsafe API was used.

## Sinks & patterns (grep, then trace to user input)
- **Command exec**: `os.system`, `subprocess.*(..., shell=True)`, `os.popen` — shell=True + user input = injection.
- **Code eval**: `eval`, `exec`, `pickle.loads`, `yaml.load` (without `SafeLoader`), `marshal` — deserialization/eval RCE.
- **SQL**: raw/f-string queries, `.raw()`, `.extra()`, `cursor.execute("... %s" % x)` — use params, not formatting.
- **SSRF**: `requests.get`/`urllib`/`httpx` on a user URL (→ `web-ssrf`).
- **Path/upload**: `open`/`send_file`/`os.path.join` with user paths (traversal); zip extraction (zip-slip).
- **Template (SSTI)**: `render_template_string`, Jinja from user input (→ `web-ssti`).
- **Secrets**: hardcoded keys/passwords; `DEBUG=True` in prod.

## Framework specifics
- **Django**: `mark_safe`/`|safe` (XSS), `.raw()`/`.extra()` (SQLi), `DEBUG=True` (info leak),
  `SECRET_KEY` exposure (session forgery), missing `@login_required`/object-level checks (IDOR),
  `ALLOWED_HOSTS='*'`, pickle session serializer.
- **Flask**: `render_template_string` (SSTI), `debug=True` (Werkzeug console RCE), weak `SECRET_KEY`
  (session tampering — `flask-unsign`), `send_file` traversal.
- **FastAPI**: missing dependency-injected auth on routes, over-broad CORS, Pydantic not enforcing
  server-side authz (BOLA at the data layer).

## Method
`rg -n "shell=True|eval\(|exec\(|pickle.loads|yaml.load\(|render_template_string|\.raw\(|\.extra\("`;
run `bandit -r .` and `semgrep --config auto`; triage by exploitable source→sink.

## Gotchas
- `yaml.safe_load` and parameterized ORM queries are the safe variants — confirm which is used.
- Bandit is noisy; rank by user-controllable input reaching the sink.

## References
Bandit; Semgrep Python rules; OWASP Django/Flask cheat sheets.
