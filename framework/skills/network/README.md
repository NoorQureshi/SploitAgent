# Network & services — `network` skills

Non-web network services, protocol attacks, and pivoting/tunneling primitives. (Open for contributions.)

Add a skill here:
```bash
cp -r framework/skills/_templates/technique.md framework/skills/network/<slug>/SKILL.md
# edit frontmatter (domain: network) + body, then:
ronin validate && ronin catalog
```

Naming: domain-prefixed kebab-case, e.g. `network-<thing>`. See the full table in [`CATALOG.md`](../../../CATALOG.md).
