# SploitAgent — operating guide for AI agents

You are an AI agent (Claude Code, Codex, Gemini, or any other) working with SploitAgent, a library of
security skills. This file tells you how to use it. Keep it short in your head: **confirm scope →
pick the skill that matches the task → follow it → prove impact → report.**

## What you have here
- `skills/<domain>/<slug>/SKILL.md` — 124 trigger-loaded skills across 19 domains (offensive **and**
  defensive). Each has a `description:` that says *when* to load it, and a body that teaches the mechanism.
- `CATALOG.md` — the full, browsable index of every skill.
- `COVERAGE.md` — how skills map to OWASP / MITRE ATT&CK / CWE.
- `methodology.md` — the full engagement method (this file is the short version).

## Rule zero — scope, always first
Never scan, request, or exploit anything outside a **confirmed authorization envelope**. Before you
touch a target, load `skills/tradecraft/tradecraft-scope-roe/SKILL.md` and confirm one of:
a signed pentest scope, a bug-bounty program the target is in scope for, or systems the user owns.
**If scope is unclear, STOP and ask the user.** Never touch out-of-scope or third-party systems.

## How to pick a skill
Match the task in front of you to a skill's `description:` trigger line (skim `CATALOG.md`, or
grep `skills/`). Load that one `SKILL.md` and work its sections in order:
**When it applies · Why it works · Method (exact commands) · Gotchas · Verify success.**
Work one lead at a time; load the next skill as new leads appear.

## The loop (how to work a target)
1. **Set up** — create the engagement workspace (below); write `scope.txt` (+ `roe.md` for bug bounty).
2. **Recon** — `recon-*` (subdomains, DNS, content/JS discovery, OSINT, services).
3. **Attack surface** — route by domain: web → `web-*`, APIs → `api-*`, cloud → `cloud-*`,
   mobile → `mobile-*`, Active Directory → `ad-*`, perimeter/appliances → `network-*`,
   Wi-Fi → `wireless-*`, LLM/AI targets → `ai-ml/*`, source → `code-review-*`,
   binaries/firmware → `reverse-engineering-*`.
4. **Foothold** — drive a weakness to proven impact; combine small bugs with `exploit-chaining`.
5. **Escalate & pivot** — `privesc-*`, `ad-*`, `network-pivoting-tunneling`.
6. **Report** — validate first with `reporting-triage-validation`, then `reporting-bug-bounty-writeup`
   or `reporting-pentest-report`.
7. **Defend** (if asked) — `defense-*` (detection, hardening, DFIR, threat modeling).

**Human-factor work** (`social-eng-*`) is a separate, **pentest-only** track with stricter
authorization — load `social-eng-methodology` first and never run it on a bug-bounty target.

## Per-engagement structure (create this, keep it tidy)
For each target, work inside its own folder so notes and loot never mix or leak:

```
engagements/<target>/
  scope.txt      # authorized targets — the hard boundary
  roe.md         # bug-bounty rules of engagement (rate limits, don'ts, disclosure)
  notes.md       # timestamped running log — the source of truth for the report
  findings/      # confirmed findings + evidence, one file per finding
  loot/          # captured data / artifacts
```

These paths are git-ignored, so an engagement run inside a clone never pollutes the repo. Keep
`notes.md` to the teach-the-mechanism standard in `methodology.md` (goal · command · result ·
why it worked · next lead).

## House rules
- Teach the mechanism, don't just paste payloads. Prove impact with the least data/action needed.
- Minimize footprint; clean up test artifacts (accounts, uploads).
- Authorized use only — this library is for pentest engagements, bug-bounty programs, and defense.
