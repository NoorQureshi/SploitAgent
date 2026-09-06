# Reporting — `reporting` skills

Turning findings into deliverables: bug-bounty reports, CVSS/VRT severity, disclosure hygiene, and CTF/pentest write-ups.

Add a skill here:
```bash
cp -r framework/skills/_templates/technique.md framework/skills/reporting/<slug>/SKILL.md
# edit frontmatter (domain: reporting) + body, then:
ronin validate && ronin catalog
```

Naming: domain-prefixed kebab-case, e.g. `reporting-<thing>`. See the full table in [`CATALOG.md`](../../../CATALOG.md).
