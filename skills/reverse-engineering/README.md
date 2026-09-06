# Reverse engineering — `reverse-engineering` skills

Understanding compiled and obfuscated artifacts: native binary triage, deobfuscation of packed/
minified/WASM/JSVMP code, and firmware extraction & analysis. Feeds `exploit-dev`, `privesc`, and
`network-appliance-attacks`.

Add a skill here:
```bash
cp -r skills/_templates/technique.md skills/reverse-engineering/<slug>/SKILL.md
# edit frontmatter (domain: reverse-engineering) + body, then:
python3 tools/catalog.py
```

Naming: domain-prefixed kebab-case, e.g. `reverse-eng-<thing>`. See the full table in [`CATALOG.md`](../../CATALOG.md).
