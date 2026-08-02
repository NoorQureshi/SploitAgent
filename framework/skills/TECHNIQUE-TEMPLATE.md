---
name: tech-REPLACE-ME
description: >
  REPLACE — one line: what this technique is and WHEN it should load. Pack in the
  trigger signals: service/version, vuln class, tool-output patterns, error strings.
  Auto-triggering depends entirely on this line. Authorized-lab framing. Example:
  "Turn a blind SSRF into RCE via gopher:// to an internal Redis; load when SSRF is
  confirmed and Redis/6379 or a queue service is reachable."
---

# <Technique name>

## When it applies
Preconditions that must be true (access level, reachable service, vuln confirmed).

## Why it works
2–3 sentences on the mechanism — so it's understood, not just copy-pasted.

## Method
1. Step, with the exact command / payload shape.
2. Next step.

## Tools
The specific tools/wordlists/PoCs involved, and the fastest option.

## Gotchas
Common failure modes and how to tell them apart from "not vulnerable".

## Verify success
The concrete signal that tells you it worked.

## Learned on
<box name / date> — reference back to the notes for the full worked example.
