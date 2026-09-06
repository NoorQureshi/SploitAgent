# Active Directory — `ad` skills

Domain attacks: Kerberos (roasting, delegation), ACL abuse, ADCS, DCSync, BloodHound-driven paths, and lateral movement.

Add a skill here:
```bash
cp -r framework/skills/_templates/technique.md framework/skills/ad/<slug>/SKILL.md
# edit frontmatter (domain: ad) + body, then:
ronin validate && ronin catalog
```

Naming: domain-prefixed kebab-case, e.g. `ad-<thing>`. See the full table in [`CATALOG.md`](../../../CATALOG.md).
