# Web application — `web` skills

Web app vulnerability classes: XSS, SQLi, SSRF, SSTI, IDOR, auth/JWT, file upload, deserialization, and concrete exploit chains.

Add a skill here:
```bash
cp -r framework/skills/_templates/technique.md framework/skills/web/<slug>/SKILL.md
# edit frontmatter (domain: web) + body, then:
ronin validate && ronin catalog
```

Naming: domain-prefixed kebab-case, e.g. `web-<thing>`. See the full table in [`CATALOG.md`](../../../CATALOG.md).
