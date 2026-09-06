# Skills library

The heart of Ronin: trigger-tagged skills an AI operator auto-loads for the task at hand.
Each skill is `framework/skills/<domain>/<slug>/SKILL.md` with schema-validated frontmatter;
its `description:` line is written so it loads on the right signals (service, vuln class,
error string, port).

**Browse the full table in [`CATALOG.md`](../../CATALOG.md)** (generated). This file is the map.

## How skills are organized — domain × type × stability

- **Domain** (the folder) — where the skill lives: `recon web api mobile cloud network ad
  ai-ml code-review exploit-dev privesc defense payloads reporting automation tradecraft`.
- **Type** (`type:`) — `arsenal` (tool selection), `technique` (a concrete chain),
  `methodology` (how to operate), `checklist`, `reference` (payloads/tables).
- **Stability** (`stability:`) — the locked/learning split that keeps Ronin reliable:
  - 🔒 **locked** — curated core (arsenals, methodology, reference). Change deliberately
    (`bin/unlock.sh` → edit → `ronin build` → `bin/lock.sh`).
  - ✍️ **learning** — the open contribution surface. New techniques land here.
- **Modes** (`modes:`) — the authorization envelope a skill is valid in: `ctf`, `bugbounty`,
  `defense`. The scope rule in `tradecraft-scope-roe` gates these.

## Mappings power the coverage view

Skills carry optional `owasp` / `owasp_llm` / `owasp_api` / `mitre` / `cwe` / `severity`
fields. `ronin catalog` rolls these into `data/skills_index.json` so coverage (OWASP Top 10,
LLM Top 10, ATT&CK) can be measured and gaps found.

## Add a skill (most welcome PR)

```bash
cp framework/skills/_templates/technique.md framework/skills/<domain>/<slug>/SKILL.md
# fill in frontmatter (strong trigger signals!) + body, then:
ronin validate      # schema check
ronin catalog       # regenerate CATALOG.md + index + discovery symlinks
```

House voice: terse, teach-the-mechanism — *when it applies · why it works · method (exact
commands + flag gloss) · gotchas · verify success*. No real targets/creds/flags. See each
domain's `README.md` for what belongs there, and `CONTRIBUTING.md` for the checklist.
