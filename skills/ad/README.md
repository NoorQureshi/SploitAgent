# Active Directory — `ad` skills

Domain attacks: Kerberos (roasting, delegation), ACL abuse, ADCS, DCSync, BloodHound-driven paths, and lateral movement.

Add a skill here:
```bash
cp -r skills/_templates/technique.md skills/ad/<slug>/SKILL.md
# edit frontmatter (domain: ad) + body, then:
python3 tools/catalog.py
```

Naming: domain-prefixed kebab-case, e.g. `ad-<thing>`. See the full table in [`CATALOG.md`](../../CATALOG.md).
