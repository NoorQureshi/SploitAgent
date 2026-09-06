# API — `api` skills

REST/GraphQL/gRPC attacks: BOLA/BFLA, mass assignment, injection, introspection abuse — the OWASP API Top 10 surface.

Add a skill here:
```bash
cp -r skills/_templates/technique.md skills/api/<slug>/SKILL.md
# edit frontmatter (domain: api) + body, then:
python3 tools/catalog.py
```

Naming: domain-prefixed kebab-case, e.g. `api-<thing>`. See the full table in [`CATALOG.md`](../../CATALOG.md).
