# Skills library — index

How skills are used: before acting, consult the matching skill for the current phase.
Each skill lives in `<slug>/SKILL.md`; its `description:` line is written so it auto-loads
on the right signals (service, vuln class, error string).

The library has two halves — **locked** and **learning**:

## 🔒 Reference skills — LOCKED (stable; don't edit during an engagement)
Curated methodology + tool arsenals. Part of the stable core; change only deliberately
(`bin/unlock.sh` → edit → `adapters/build.sh all` → `bin/lock.sh`).

- **htb-insane** — structure & rabbit-hole discipline for hard/Insane multi-stage boxes.
- **tools-recon** — port/host/service discovery (nmap, rustscan, DNS/vhost, SMB/RPC, SNMP, NFS).
- **tools-web** — web enum + exploitation (content/param discovery, nuclei, sqlmap, NoSQLi, LFI/SSTI/SSRF, JWT).
- **tools-privesc** — Linux + Windows local privesc (linpeas/winPEAS, sudo/SUID/caps, potato family, shell/transfer).
- **tools-ad-pivot** — Active Directory, pivoting/tunneling, password cracking (BloodHound, netexec, impacket, certipy, ligolo/chisel, hashcat).

## ✍️ Technique skills — LEARNING (this is where the framework grows)
Narrow, trigger-tagged chains captured by the **learn** role as boxes teach them. This is the
**only** part of the framework written to while working a box. Add one:
`cp TECHNIQUE-TEMPLATE.md tech-<slug>/SKILL.md`, fill it in, add a line below, then
`./adapters/build.sh all`.

- **tech-mongo-agg-facet-bypass** — MongoDB aggregation stage-allowlist bypass via `$facet`→`$unionWith` to read sibling collections (trigger: user-supplied `pipeline` param, "use the pipeline parameter" error, Node+Mongo). *[AEGIS]*
- **tech-webauthn-software-authenticator** — register/log in to a WebAuthn RP with a self-built software authenticator when attestation is `none` (trigger: FIDO2/passkey login, `/webauthn/*/begin|finish`, an invite/enroll token in hand). *[AEGIS]*
- **tech-gopher-redis-rce** — SSRF → internal unauth Redis → RCE via `gopher://` (cron / SSH key / webshell) (trigger: confirmed SSRF + Redis/6379 reachable).
