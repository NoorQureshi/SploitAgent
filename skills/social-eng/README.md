# Social engineering — `social-eng` skills

Authorized human-factor testing: phishing, vishing/pretexting, and physical assessment — measured
to improve awareness and controls, never to embarrass people. **`pentest`-only, and stricter on
authorization than any other domain.**

> Load [`social-eng-methodology`](social-eng-methodology/SKILL.md) **first**. Social engineering
> tests real people, so it requires written sign-off from someone empowered to consent for the
> staff being tested, agreed pretext/target boundaries, a no-harm line, and a carried authorization
> letter for physical work. No consent → do not run it.

Add a skill here:
```bash
cp -r skills/_templates/methodology.md skills/social-eng/<slug>/SKILL.md
# edit frontmatter (domain: social-eng, modes: [pentest]) + body, then:
python3 tools/catalog.py
```

Naming: domain-prefixed kebab-case, e.g. `social-eng-<thing>`. See the full table in [`CATALOG.md`](../../CATALOG.md).
