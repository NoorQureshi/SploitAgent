# Reconnaissance — `recon` skills

Passive/active enumeration, OSINT, subdomain discovery, tech fingerprinting, content/param discovery — building the attack surface before you touch it.

Add a skill here:
```bash
cp -r skills/_templates/technique.md skills/recon/<slug>/SKILL.md
# edit frontmatter (domain: recon) + body, then:
python3 tools/catalog.py
```

Naming: domain-prefixed kebab-case, e.g. `recon-<thing>`. See the full table in [`CATALOG.md`](../../CATALOG.md).
