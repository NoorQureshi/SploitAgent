# Defense / blue-team — `defense` skills

Detection engineering (Sigma/ATT&CK), hardening baselines, and DFIR/triage — the defensive half of the library.

Add a skill here:
```bash
cp -r skills/_templates/technique.md skills/defense/<slug>/SKILL.md
# edit frontmatter (domain: defense) + body, then:
python3 tools/catalog.py
```

Naming: domain-prefixed kebab-case, e.g. `defense-<thing>`. See the full table in [`CATALOG.md`](../../CATALOG.md).
