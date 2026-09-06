# Engagement methodology

The operating method behind SploitAgent's skills: the loop, the scope rule, the note-taking
standard, and the working principles. It's tool-neutral — the same whether you drive it with
Claude Code, Codex, Gemini, a local model, or by hand.

For **authorized security work only** — penetration-testing engagements, bug-bounty programs
you're in scope for, and defensive assessment of systems you own or are authorized to test.

## The hard rule — scope
Operate only inside a **confirmed authorization envelope**. The `tradecraft-scope-roe` skill
governs this in full — load it first. In short:
- **Pentest / engagement:** the signed scope (statement of work / authorization) names the
  in-scope assets and the window. Practice ranges you own or are licensed to test count here.
- **Bug bounty:** the program's in-scope assets + rules of engagement; out-of-scope is a hard block.
- **Defensive:** assets your organization owns or authorizes you to assess.

Before any scan, request, or exploit: if the target isn't clearly inside a confirmed envelope,
**stop and confirm authorization**. Never touch out-of-scope, third-party, or unauthorized
infrastructure. Match every action to an in-scope asset and stay within the rules of engagement.
Record the confirmed targets in `scope.txt` and treat it as a hard boundary for every phase.

## The loop (phases)
1. **Set up.** Confirm scope, write `scope.txt` (and `roe.md` for bug bounty), start `notes.md`.
2. **Recon.** Map the attack surface: subdomains/hosts, services, and content. Skills:
   `recon-subdomain-enum`, `recon-content-discovery`, `recon-osint`, `recon-js-analysis`,
   `recon-arsenal`, `network-service-attacks`.
3. **Attack surface → route each lead.** Web to the `web-*` skills; APIs to `api-*`; cloud to
   `cloud-*`; mobile to `mobile-*`; Active Directory to `ad-*`; source you can read to
   `code-review-*`. Load the skill whose trigger matches the signal.
4. **Foothold / proof.** Drive a weakness to demonstrated impact; capture reproducible evidence.
   Chain small bugs into real impact with `exploit-chaining`.
5. **Escalate & pivot.** `privesc-arsenal` for local escalation; `network-pivoting-tunneling`
   and `ad-*` for lateral movement. On complex, multi-host targets, apply
   `tradecraft-complex-engagements` for structure and dead-end discipline.
6. **Report.** Compile findings with correct severity and clean evidence — `reporting-bug-bounty-writeup`.
7. **Defend (as applicable).** Turn findings into fixes and detections — `defense-hardening-baseline`,
   `defense-detection-sigma`, `defense-dfir-triage`.

## Consult and grow the skills library
Skills live by domain at `skills/<domain>/<slug>/SKILL.md`; browse them all in `CATALOG.md`.
- Before exploiting anything, load the matching skill for the current vuln class / domain (an
  `arsenal` for tool selection, a `technique` for a known chain) and apply it.
- On complex, multi-stage targets, `tradecraft-complex-engagements` governs structure and
  dead-end discipline.
- When work teaches a reusable technique, capture it as a new `stability: learning` technique
  skill under the right domain (from `skills/_templates/technique.md`) so future work
  auto-applies it, then run `python3 tools/catalog.py`.

## Note-taking standard (teach, don't just log)
`notes.md` is a **learning document**, not a command dump. A future reader should understand
*why it worked*, not only *that* it worked. Every meaningful step gets a short block:
1. **Goal / why now** — what you were trying to learn or achieve, and the finding that pointed here.
2. **Tool & exact syntax** — the actual command, with a one-line gloss of the flags that matter,
   and *why that tool* over alternatives when the choice is instructive.
3. **Result** — the relevant output (trimmed), not a wall of text.
4. **Why it worked / what it means** — the *mechanism*: why an IDOR is possible, why a capability
   grants root, why a payload lands. This is the part worth learning.
5. **Next lead** — the single concrete action this unlocks.

Also capture **what you tried that failed and why**, and **decision points**. Explain terms of
art the first time. Favor plain-language mechanism over jargon.

## Locked core vs learning library
SploitAgent improves without corrupting what makes it reliable:
- 🔒 **Locked core (stable):** `methodology.md`, the arsenals, and the tradecraft/scope skills
  (`stability: locked`). Change deliberately, with rationale in the PR.
- ✍️ **Learning library (grows):** every `stability: learning` skill. This is the open, welcome
  contribution surface. Add here; keep the core stable.

## Working principles
Enumerate first — when stuck, the answer is almost always "enumerate more," not a bigger
exploit. Log every meaningful command and finding. Track dead-ends with the reason each was
ruled out. Prove impact with the least data/action needed; minimize footprint and clean up.
Explain your reasoning as you go — the reasoning is the skill. End each step with one clear next action.
