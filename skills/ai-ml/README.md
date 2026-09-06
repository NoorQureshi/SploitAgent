# AI / LLM — `ai-ml` skills

Attacks on LLM-backed apps and agents: prompt injection (direct/indirect), data exfil, tool/function abuse, jailbreaks — OWASP LLM Top 10.

Add a skill here:
```bash
cp -r skills/_templates/technique.md skills/ai-ml/<slug>/SKILL.md
# edit frontmatter (domain: ai-ml) + body, then:
python3 tools/catalog.py
```

Naming: domain-prefixed kebab-case, e.g. `ai-ml-<thing>`. See the full table in [`CATALOG.md`](../../CATALOG.md).
