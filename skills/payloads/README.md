# Payloads — `payloads` skills

Curated payload sets and bypass tables: polyglots, WAF evasion, and wordlist pointers referenced by the technique skills. (Open for contributions.)

Add a skill here:
```bash
cp -r skills/_templates/technique.md skills/payloads/<slug>/SKILL.md
# edit frontmatter (domain: payloads) + body, then:
python3 tools/catalog.py
```

Naming: domain-prefixed kebab-case, e.g. `payloads-<thing>`. See the full table in [`CATALOG.md`](../../CATALOG.md).
