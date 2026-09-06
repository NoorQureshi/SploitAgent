# Contributing to Ronin

Thanks for helping grow the library. Ronin is for **authorized** security work only —
penetration-testing engagements, bug-bounty programs you're in scope for, and defensive
assessment of systems you own or are authorized to test. Every contribution must keep that
framing: no real targets, no live credentials/secrets, no content aimed at systems you don't
own or aren't authorized to test.

## What a contribution is

Ronin is a **library of skills**. A contribution is almost always a new (or improved)
`skills/<domain>/<slug>/SKILL.md`. There's no build step and no CLI to learn — skills are plain
Markdown with a validated frontmatter block. The one script, `tools/catalog.py`, validates skills
and regenerates the catalog.

## Add a skill (the common PR)

Domains: `recon web api mobile cloud network ad ai-ml code-review exploit-dev privesc defense
payloads reporting automation tradecraft`.

```bash
cp skills/_templates/technique.md skills/<domain>/<slug>/SKILL.md
# (arsenal.md / methodology.md templates also available)
python3 tools/catalog.py validate   # schema-check your frontmatter
python3 tools/catalog.py            # validate + regenerate CATALOG.md
```

Fill it in:
- **Frontmatter** — required: `name` (domain-prefixed kebab-case, e.g. `web-ssrf`), `description`,
  `domain`, `type`, `stability`, `modes` (`pentest`/`bugbounty`/`defense`), `schema_version: 1`.
  Encouraged: `severity`, `owasp`/`owasp_llm`/`owasp_api`, `mitre`, `cwe`, `tools`.
- **`description:`** must pack concrete **trigger signals** (service/version, vuln class,
  tool-output patterns, error strings, ports) — auto-loading is only as good as this line.
- **Body:** *when it applies · why it works (the mechanism) · method (exact commands + flag gloss)
  · gotchas · verify success · references.*
- Generalize: no real IPs/creds/secrets. Big payload lists go in a `reference/` subfolder next to
  the `SKILL.md`, not inline.

`CATALOG.md` and `data/skills_index.json` are **generated** — don't hand-edit them; run
`tools/catalog.py` and commit the regenerated `CATALOG.md`.

## Locked core vs learning library
- 🔒 **Locked core** — `methodology.md`, the `*-arsenal` skills, and the tradecraft/scope skills
  (`stability: locked`). Changing these changes behaviour; do it deliberately and explain *why* in
  your PR.
- ✍️ **Learning library** — every skill tagged `stability: learning`. New techniques land here —
  the easiest and most welcome contribution.

## Before you open a PR

```bash
python3 -m py_compile tools/catalog.py
python3 tools/catalog.py validate                       # skills pass the schema
python3 tools/catalog.py && git diff --quiet -- CATALOG.md && echo "catalog up to date ✓"
```

Checklist:
- [ ] Skill under the right `skills/<domain>/`, frontmatter passes `tools/catalog.py validate`.
- [ ] Authorized-use framing; correct `modes:`; no real targets/creds/secrets.
- [ ] Strong trigger signals in `description:`; mappings (`owasp`/`mitre`/`cwe`) where they apply.
- [ ] `CATALOG.md` regenerated and committed; CI is green.

## Style
Match the house voice: terse, teach-the-mechanism — *tool · why over alternatives · exact command
with a flag gloss · gotcha*. Explain the mechanism, not just the command. Small focused skills beat
one giant file.
