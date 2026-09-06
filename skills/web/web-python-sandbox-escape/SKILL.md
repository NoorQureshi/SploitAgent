---
name: web-python-sandbox-escape
description: >
  Escape a Python sandbox / eval jail to reach code execution — defeat keyword blocklists and
  restricted eval/exec by reaching objects through the class hierarchy. Load when user input hits
  eval/exec/a "safe" expression evaluator, a Python REPL/calculator feature, a template that runs
  Python, or a filtered code box. Signals: "eval", "exec", `__import__` blocked, banned words
  (import/os/system), a Python jail, PyYAML/pickle input, a formula/expression field.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: critical
owasp: [A03:2021-Injection]
cwe: [CWE-94, CWE-95, CWE-265]
tools: [python]
schema_version: 1
---

# Python sandbox / eval escape

## When it applies
User input reaches `eval()`, `exec()`, a "safe expression" evaluator, a template engine that runs
Python, or a feature that runs user formulas — and a blocklist tries to make it safe by banning
words like `import`, `os`, or `system`. If you can evaluate Python at all, the blocklist is almost
always bypassable.

## Why it works
String-based keyword filters remove *names*, but the objects they'd name are still reachable through
Python's object graph. From any object you can walk `__class__ → __base__ → __subclasses__()` to
find a class whose module gives you code execution (`subprocess.Popen`, `os.system`, `builtins`),
without ever typing a banned identifier literally.

## Method
1. **Confirm evaluation.** Send an arithmetic probe (`7*7` → `49`) or a type leak (`().__class__`)
   to prove Python is evaluating your input.
2. **Reach the class tree.** From a literal you're allowed:
   `().__class__.__base__.__subclasses__()` — enumerate to find a useful class (look for
   `subprocess.Popen`, `os._wrap_close`, `warnings.catch_warnings` → `builtins`). Index into the
   list once you know the position.
3. **Execute** via the found class, e.g. (index varies per build):
   `().__class__.__base__.__subclasses__()[N]('id',shell=True,stdout=-1).communicate()`.
4. **Defeat banned identifiers** without typing them:
   - Attribute by string: `getattr(obj,'sys'+'tem')`.
   - Build names from chars: `"__imp"+"ort__"`, `chr(...)`, or index into strings.
   - Reach builtins: `().__class__.__base__.__subclasses__()[i].__init__.__globals__['__builtins__']`.
5. **Alternate sinks** — if the input is YAML/pickle rather than eval: unsafe `yaml.load` and
   `pickle.loads` execute `__reduce__`; `str.format`/f-string on attacker templates can read
   object internals (`{0.__class__}`) → info leak → escalate.

## Gotchas
- **`__subclasses__()` ordering is not stable** across Python versions/builds — enumerate at runtime
  to find your target's index, don't hardcode it.
- **Blocklist vs allowlist** — a true AST allowlist (only permitted nodes) is far harder; test
  whether attribute access / subscripting is even parsed before going deep.
- **`eval` with restricted `__builtins__`** still leaks via the class tree — that's the whole point.
- This overlaps `web-ssti` (Jinja uses the same gadget) — if it's a template, start there.

## Verify success
Command output from the host (e.g. `id`, a file read) returned through the evaluator, proving code
execution past the sandbox — not just a leaked class name.

## References
"Python jail escape" / pyjail write-ups; PayloadsAllTheThings (Python sandbox); CWE-94/95.
