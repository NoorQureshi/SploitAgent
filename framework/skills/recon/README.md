# Reconnaissance — `recon` skills

Passive/active enumeration, OSINT, subdomain discovery, tech fingerprinting, content/param discovery — building the attack surface before you touch it.

Add a skill here:
```bash
cp -r framework/skills/_templates/technique.md framework/skills/recon/<slug>/SKILL.md
# edit frontmatter (domain: recon) + body, then:
ronin validate && ronin catalog
```

Naming: domain-prefixed kebab-case, e.g. `recon-<thing>`. See the full table in [`CATALOG.md`](../../../CATALOG.md).
