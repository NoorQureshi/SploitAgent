# Web application — `web` skills

Web app vulnerability classes: XSS, SQLi, SSRF, SSTI, IDOR, auth/JWT, file upload, deserialization, and concrete exploit chains.

Add a skill here:
```bash
cp -r skills/_templates/technique.md skills/web/<slug>/SKILL.md
# edit frontmatter (domain: web) + body, then:
python3 tools/catalog.py
```

Naming: domain-prefixed kebab-case, e.g. `web-<thing>`. See the full table in [`CATALOG.md`](../../CATALOG.md).
