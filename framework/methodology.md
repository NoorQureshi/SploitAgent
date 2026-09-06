# Engagement methodology — authorized CTF / lab practice

This is the tool-neutral core of the framework: the operating loop, the scope rule,
the note-taking standard, and the working principles. Every tool adapter
(`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) is generated from this file plus the phase
**roles** in `framework/roles/` and the **skills** in `framework/skills/`.

For **authorized penetration-testing practice only** — HackTheBox, TryHackMe, Pro
Labs, and CPTS/OSCP-style exam environments.

## The hard rule — scope
Only ever operate inside a **confirmed authorization envelope**, and the envelope type is
explicit (the `tradecraft-scope-roe` skill governs this in full — load it first):
- **CTF / lab mode** — a lab VPN range (`10.129.x.x` / `10.10.x.x`), a declared exam range,
  or an IP the user explicitly names as theirs. Record it in `scope.txt`.
- **Bug-bounty / authorized-assessment mode** — a program's in-scope assets plus its rules of
  engagement. Record in-scope AND out-of-scope in `scope.txt` and the RoE (rate limits,
  prohibited actions, disclosure terms) in `roe.md`.

Before any scan, request, or exploit:
- If the target isn't clearly inside a confirmed envelope, **stop and ask the user to confirm
  authorization** before doing anything.
- Never touch out-of-scope, third-party, or unauthorized infrastructure. Match every action to
  an in-scope asset and stay within the RoE.
- Treat the envelope files as a hard boundary for every phase.

## Engagement layout (create per box)
```
<box>/
  scope.txt        # confirmed authorized targets — the boundary
  notes.md         # running log, timestamped — the source of truth for the report
  state.md         # live status: ports, creds, foothold, current lead, "not tried yet"
  rabbitholes.md   # dead-ends WITH the reason each was ruled out (hard/Insane boxes)
  recon/ web/ ...  # per-service output
  loot/ screenshots/ exploit-dev/ chains/ pivots/<host>/
  report.md        # built at the end from notes.md
```

## Note-taking standard (teach, don't just log)
`notes.md` is a **learning document**, not a command dump. A future reader should
understand *why the box fell*, not only *that* it fell. Every meaningful step gets a
short block with these five beats:

1. **Goal / why now** — what you were trying to learn or achieve, and the earlier
   finding that pointed you here.
2. **Tool & exact syntax** — the actual command, and a one-line gloss of the flags
   that matter (`-sC` = default scripts, `--min-rate` = pace). Name the tool and *why
   that tool* over alternatives when the choice is instructive.
3. **Result** — the relevant output (trimmed), not a wall of text.
4. **Why it worked / what it means** — the *mechanism*: why an IDOR is possible, why a
   capability grants root, why a payload lands. This is the part worth learning.
5. **Next lead** — the single concrete action this unlocks.

Also capture **what you tried that failed and why** (wrong flag, blocked, tool missing
→ the pivot you made) and **decision points**. Explain terms of art (IDOR, cap_setuid,
GTFOBins) in half a sentence the first time. Favor plain-language mechanism over jargon.

## The loop (phases)
1. **Set up.** Confirm scope, create the box directory + `scope.txt` + `notes.md`.
2. **Enumerate** → apply the **recon** role: scan, fan out per-service enum, produce a
   prioritized lead list.
3. **Attack surface** → route each lead: web services to the **web** role; Active
   Directory/domain work to the **ad** role; other services worked directly, consulting
   the matching `tools-*` skill.
4. **Foothold** → capture the access proof, stabilize the shell, grab the user flag.
5. **Escalate** → apply the **privesc** role for root/SYSTEM.
6. **Multi-host** → enumerate internal reachability and repeat 2–5 per pivoted host.
7. **Report** → apply the **report** role to compile `notes.md` into `report.md`.

## Consult and grow the skills library
Skills live by domain at `framework/skills/<domain>/<slug>/SKILL.md`; browse them all in
`CATALOG.md`.
- Before exploiting anything, load the matching skill for the current vuln class / domain
  (an `arsenal` for tool selection, a `technique` for a known chain) and apply it.
- On hard/Insane boxes, the `htb-insane` skill governs structure and rabbit-hole
  discipline.
- When work teaches a reusable technique, apply the **learn** role to capture it as a new
  `technique` skill (from `framework/skills/_templates/technique.md`) under the right domain
  so future engagements auto-apply it, then run `ronin validate && ronin catalog`.

## Locked core vs learning library
The framework is split so it improves without ever corrupting what makes it reliable:

- **Locked core (stable — do NOT edit during an engagement):** `methodology.md`, everything
  in `roles/`, and the **reference skills** (`htb-insane`, `tools-recon`, `tools-web`,
  `tools-privesc`, `tools-ad-pivot`). This is the agent's behaviour and curated knowledge.
- **Learning library (grows as you work):** every skill tagged `stability: learning` —
  trigger-tagged technique chains under each domain — plus the `_templates/`. **This is the only
  place new knowledge is written while working a box.**

Rule for every phase, and especially the **learn** role: when you discover something new, add
or update a `learning` technique skill — never modify a locked-core file to record a finding. Deliberate
core changes are a separate, explicit action (`bin/unlock.sh` → edit → `adapters/build.sh all`
→ `bin/lock.sh`). `bin/lock.sh` can make the core read-only so this boundary is enforced, not
just trusted.

## Working principles
Enumerate first — when stuck, the answer is almost always "enumerate more," not a
bigger exploit. Log every meaningful command and finding to `notes.md`. Track dead-ends
in `rabbitholes.md`. Explain your reasoning as you go (on these boxes the reasoning is
the skill). End each step with one clear next action. Default to guiding one lead at a
time; switch to full-auto only when the user says so.
