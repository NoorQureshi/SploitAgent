# Automation — `automation` skills

Repeatable pipelines: recon automation, nuclei templates, continuous monitoring, and CI-style hunting. (Open for contributions.)

Add a skill here:
```bash
cp -r skills/_templates/technique.md skills/automation/<slug>/SKILL.md
# edit frontmatter (domain: automation) + body, then:
python3 tools/catalog.py
```

Naming: domain-prefixed kebab-case, e.g. `automation-<thing>`. See the full table in [`CATALOG.md`](../../CATALOG.md).
