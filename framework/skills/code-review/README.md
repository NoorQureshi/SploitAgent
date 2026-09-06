# Source-code review — `code-review` skills

SAST-style manual review: dangerous sinks per language, secret detection, auth/authz flaws, and vulnerable dependency patterns. (Open for contributions.)

Add a skill here:
```bash
cp -r framework/skills/_templates/technique.md framework/skills/code-review/<slug>/SKILL.md
# edit frontmatter (domain: code-review) + body, then:
ronin validate && ronin catalog
```

Naming: domain-prefixed kebab-case, e.g. `code-review-<thing>`. See the full table in [`CATALOG.md`](../../../CATALOG.md).
