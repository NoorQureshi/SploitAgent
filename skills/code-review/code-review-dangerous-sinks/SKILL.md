---
name: code-review-dangerous-sinks
description: >
  Grep-ready dangerous function/sink catalog per language for fast code review. Load when
  reviewing source in PHP, Python, JavaScript/Node, Java, Ruby, Go, .NET/C# and you need the
  exact functions that cause RCE/SQLi/SSRF/traversal/deserialization. Signals: "dangerous
  functions", "sinks", grepping a codebase.
domain: code-review
type: reference
stability: learning
modes: [bugbounty, defense]
severity: info
cwe: [CWE-78, CWE-89, CWE-94, CWE-502, CWE-22]
tools: [ripgrep, semgrep]
schema_version: 1
---

# Dangerous sinks by language (grep catalog)

## When it applies
You're reading source and want the fastest path to bugs: grep every dangerous sink, then trace
each hit's argument back to user input.

## Why it works
A small set of functions cause most severe bugs (command/code exec, SQL, deserialization, file
access, SSRF). Enumerating them turns review into "find the sink → prove the source".

## Sinks to grep (trace the argument to a user source)
- **Command exec (RCE, CWE-78)**: PHP `system exec shell_exec passthru proc_open` · Python
  `os.system subprocess.*(shell=True) os.popen` · Node `child_process.exec execSync` · Java
  `Runtime.exec ProcessBuilder` · Ruby `` system exec `backticks` %x() `` · Go `exec.Command`.
- **Code eval (CWE-94)**: `eval` (all), Python `exec pickle.loads`, Node `Function() vm`,
  PHP `eval assert create_function preg_replace/e`, Ruby `eval send`.
- **SQL (CWE-89)**: string-built queries / concatenation into `query execute` (all ORMs have a
  raw path — grep `raw`, `.query(`, `String.format` near SQL).
- **Deserialization (CWE-502)**: Python `pickle yaml.load(!safe) marshal`, Java `readObject
  XMLDecoder`, PHP `unserialize`, Ruby `Marshal.load YAML.load`, .NET `BinaryFormatter`.
- **File/path (CWE-22)**: `open read include require fopen readFile sendFile` with user paths;
  archive extractors (zip-slip).
- **SSRF (CWE-918)**: URL fetchers — `requests.get urllib curl file_get_contents http.get
  HttpClient` taking a user URL.
- **Template (SSTI)**: `render_template_string`, Twig/Freemarker string templates.
- **Secrets**: `password= api_key= secret token=` literals; private keys.

## Method
`rg -n "os\.system|subprocess|shell_exec|eval\(|unserialize|pickle\.loads|readObject|render_template_string"`
then for each hit trace the argument. Pair with `semgrep --config auto` for dataflow.

## Gotchas
- Parameterized queries / allowlisted args = safe; confirm the source, don't report the grep hit.
- `yaml.safe_load` and framework-escaped ORMs are the safe variants — note which one is used.

## References
OWASP Code Review Guide; GTFOBins (for the exec side); Semgrep registry.
