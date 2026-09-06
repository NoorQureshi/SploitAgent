# Wireless / Wi-Fi — `wireless` skills

802.11 attacks for authorized wireless engagements: WPA2-PSK handshake/PMKID capture and cracking,
and evil-twin / rogue-AP credential harvesting against WPA2-Enterprise and captive portals.
**`pentest`-only** — wireless testing needs physical proximity and authorization for the specific
in-scope SSIDs.

Add a skill here:
```bash
cp -r skills/_templates/technique.md skills/wireless/<slug>/SKILL.md
# edit frontmatter (domain: wireless, modes: [pentest]) + body, then:
python3 tools/catalog.py
```

Naming: domain-prefixed kebab-case, e.g. `wireless-<thing>`. See the full table in [`CATALOG.md`](../../CATALOG.md).
