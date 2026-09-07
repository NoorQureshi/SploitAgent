# Cryptography — `cryptography` skills

Practical attacks on weak or misused crypto in real applications — not puzzle-solving. Weak/textbook
RSA (JWT RS256 keys, custom signatures), and symmetric oracles on encrypted tokens/cookies (CBC
padding oracle, ECB block shuffling, hash-length-extension of homemade MACs).

Add a skill here:
```bash
cp -r skills/_templates/technique.md skills/cryptography/<slug>/SKILL.md
# edit frontmatter (domain: cryptography) + body, then:
python3 tools/catalog.py
```

Naming: domain-prefixed kebab-case, e.g. `crypto-<thing>`. See the full table in [`CATALOG.md`](../../CATALOG.md).
