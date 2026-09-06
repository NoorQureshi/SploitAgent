---
name: tradecraft-scope-roe
description: >
  Establish and enforce the authorization envelope before any testing — the dual-mode scope
  rule. Load FIRST on every engagement, on "start", a new target, a program handle, or any
  ambiguity about what is allowed. Signals: a domain/IP to test, a bug-bounty program, a lab range.
domain: tradecraft
type: methodology
stability: locked
modes: [ctf, bugbounty, defense]
severity: info
schema_version: 1
---

# Scope & Rules of Engagement (the hard rule)

## When this governs
Always, before the first packet. Ronin operates only inside a confirmed authorization
envelope, and the envelope type is explicit. If scope is unclear, STOP and confirm with the
user — never "probe a little to see".

## The two envelopes
- **CTF / lab mode** — boundary is a lab range you confirmed authorized (`10.129.x.x`,
  `10.10.x.x`, a declared exam range, or an IP the user names as theirs). Record it in `scope.txt`.
- **Bug-bounty / authorized-assessment mode** — boundary is a **program scope + rules of
  engagement**. Before testing, capture:
  - `scope.txt` — exact in-scope assets (domains, wildcards, IP ranges, apps) AND explicit
    out-of-scope. Out-of-scope is a hard block, not a suggestion.
  - `roe.md` — allowed test types, rate limits, prohibited actions (no DoS, no social
    engineering unless allowed, no automated scanning if banned), data-handling rules, and the
    disclosure/safe-harbor terms.

## The discipline
1. **Confirm authorization** and write the envelope files before scanning.
2. **Match every target** against in-scope patterns at request time; anything unmatched or
   out-of-scope is refused. Third parties (shared CDNs, SaaS the target merely uses) are out.
3. **Respect RoE limits** — throttle to the program's rate cap; skip prohibited techniques.
4. **Minimize impact** — prove the class with the least data/action; no lateral movement or
   data hoarding beyond what proves the finding; clean up artifacts (uploaded files, test accounts).
5. **Mode-gate skills** — a technique tagged `ctf`-only (destructive/lab-safe-only) does not run
   during a live `bugbounty` engagement.

## Anti-patterns
- "It resolved so it's probably in scope" — verify against the program's list.
- Testing an acquisition/subsidiary not named in scope.
- Ignoring rate limits because the bug is interesting.
- Keeping real customer data as "evidence" instead of a redacted proof.

## Verify
`scope.txt` (and `roe.md` for bug bounty) exist, the user confirmed authorization, and every
planned action maps to an in-scope asset within the RoE.

## References
Program policy pages; HackerOne/Bugcrowd RoE; disclose.io safe-harbor.
