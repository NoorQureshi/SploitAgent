# Automation — `automation` skills

Repeatable pipelines: recon automation, nuclei templates, continuous monitoring, and CI-style hunting. (Open for contributions.)

Add a skill here:
```bash
cp -r framework/skills/_templates/technique.md framework/skills/automation/<slug>/SKILL.md
# edit frontmatter (domain: automation) + body, then:
ronin validate && ronin catalog
```

Naming: domain-prefixed kebab-case, e.g. `automation-<thing>`. See the full table in [`CATALOG.md`](../../../CATALOG.md).
