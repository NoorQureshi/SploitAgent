# Reporting — `reporting` skills

Turning findings into deliverables: bug-bounty reports, CVSS/VRT severity, disclosure hygiene, and pentest write-ups.

Add a skill here:
```bash
cp -r skills/_templates/technique.md skills/reporting/<slug>/SKILL.md
# edit frontmatter (domain: reporting) + body, then:
python3 tools/catalog.py
```

Naming: domain-prefixed kebab-case, e.g. `reporting-<thing>`. See the full table in [`CATALOG.md`](../../CATALOG.md).
