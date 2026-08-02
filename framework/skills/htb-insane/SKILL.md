---
name: htb-insane
description: >
  Structure and methodology for hard and Insane-rated lab machines (HackTheBox, Pro
  Labs, CPTS/OSCP-hard). Use when a box is rated Hard/Insane, when a foothold needs
  chaining multiple bugs, when work spans multiple sessions/hosts, or when you're
  deep in rabbit-holes and stuck. Adds rabbit-hole discipline, exploit chaining,
  custom-exploit workflow, and multi-host tracking on top of the base loop. Trigger
  on: "insane box", "hard box", "stuck", "rabbit hole", "chain", "pro lab", multi-host.
---

# Insane-Rated Engagement Structure

Insane boxes differ in *kind*, not just difficulty. The intended path is usually a
chain of 2–4 bugs wrapped in deliberate dead-ends, sometimes needing source review,
custom exploit work, reversing, or a crypto attack. They run long and often span
multiple hosts. Wins come from disciplined enumeration and ruthless rabbit-hole
tracking — not a bigger exploit. Authorized lab targets only (see `scope.txt`).

## Directory additions (on top of the standard layout in CLAUDE.md)
```
<box>/
  state.md          # live status + a "haven't tried yet" list
  rabbitholes.md    # dead-ends WITH the reason each was ruled out  ← Insane-critical
  chains/           # working exploit chains / PoC drafts, one link at a time
  exploit-dev/      # source review notes, custom/modified exploit work
  pivots/<host>/    # one subdir per internal host reached
```

## Extended phase model
1. **Exhaustive recon.** Every port, vhost, parameter, version string. The clue is
   often in the thing you skipped.
2. **Clue harvesting.** Log *everything*, including what looks irrelevant — odd
   headers, unusual file names, custom apps, strange responses.
3. **Foothold by chain.** Expect to combine bugs (e.g. SSRF → internal service →
   deserialization → RCE). Build it in `chains/`, verifying each link before adding
   the next.
4. **Stabilize + situational awareness.** PTY, then map users/services/internal
   network thoroughly before moving.
5. **Pivot / lateral.** Enumerate internal reachability; one `pivots/<host>/` per
   host; repeat the loop per host. See the `tools-ad-pivot` skill.
6. **Privesc (often custom).** Standard checks first, but be ready for a box-specific
   vector — a custom SUID binary, a bespoke service, an ACL path.
7. **Chain writeup.** Document the full chain end to end; each link needs
   reproduction steps and evidence.

## Rabbit-hole discipline (the Insane-specific skill)
- The moment a lead dies, write it in `rabbitholes.md` **with why** it's ruled out.
  This stops you re-walking dead-ends across a multi-day box and reveals what you
  actually haven't tried.
- Keep a live "haven't tried yet" list in `state.md`. When stuck, work that list
  before reaching for exotic exploits.
- Truly stuck? Re-run enumeration on the least-examined service, diff against earlier
  output, and re-read the clue log. The path is usually already in your notes.

## Custom-exploit workflow (authorized lab only)
Read any public PoC fully before running it; note the source in `exploit-dev/`. When
a PoC needs adapting, work in `exploit-dev/` with a clear record of what changed and
why — that becomes report content and a capture-worthy technique skill. Review
application source when you have it: auth logic, input handling, serialization, crypto.

## Capture what you learn
When a box teaches a reusable technique (a novel chain, a bespoke privesc, a crypto
attack), hand it to `htb-learn` to capture as a `tech-*` skill so future boxes
benefit. See `README.md`.

Working style: enumerate first, track dead-ends, build chains incrementally, and
explain your reasoning — on Insane boxes the reasoning *is* the skill.
