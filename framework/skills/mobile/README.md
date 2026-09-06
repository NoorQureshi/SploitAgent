# Mobile — `mobile` skills

Android/iOS assessment: static/dynamic analysis, Frida, cert-pinning bypass, insecure storage, deep-link and IPC abuse. (Open for contributions.)

Add a skill here:
```bash
cp -r framework/skills/_templates/technique.md framework/skills/mobile/<slug>/SKILL.md
# edit frontmatter (domain: mobile) + body, then:
ronin validate && ronin catalog
```

Naming: domain-prefixed kebab-case, e.g. `mobile-<thing>`. See the full table in [`CATALOG.md`](../../../CATALOG.md).
