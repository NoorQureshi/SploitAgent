# Privilege escalation — `privesc` skills

Local privilege escalation on Linux and Windows: misconfig quick-wins first, then deeper vectors toward root/SYSTEM.

Add a skill here:
```bash
cp -r skills/_templates/technique.md skills/privesc/<slug>/SKILL.md
# edit frontmatter (domain: privesc) + body, then:
python3 tools/catalog.py
```

Naming: domain-prefixed kebab-case, e.g. `privesc-<thing>`. See the full table in [`CATALOG.md`](../../CATALOG.md).
