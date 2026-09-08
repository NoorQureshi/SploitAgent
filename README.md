<div align="center">

# SploitAgent

**Security skills for AI agents.** A library of 127 security techniques (offensive + defensive) that
Claude Code — or any AI agent — loads on demand to work an **authorized** target from recon to report.

[![CI](https://github.com/NoorQureshi/SploitAgent/actions/workflows/ci.yml/badge.svg)](https://github.com/NoorQureshi/SploitAgent/actions/workflows/ci.yml)
![skills](https://img.shields.io/badge/skills-127-334155?style=flat-square)
![domains](https://img.shields.io/badge/domains-20-334155?style=flat-square)
![mapped](https://img.shields.io/badge/mapped-OWASP%20%C2%B7%20MITRE%20ATT%26CK-334155?style=flat-square)
![license](https://img.shields.io/badge/license-MIT-334155?style=flat-square)

<sub>[Docs & site](https://noorqureshi.github.io/SploitAgent/) · [How it works](https://noorqureshi.github.io/SploitAgent/interact.html) · [Search skills](https://noorqureshi.github.io/SploitAgent/catalog.html) · [Contributing](CONTRIBUTING.md)</sub>

<img src="docs/terminal.svg" width="820" alt="A Claude Code terminal session: describe a task in plain English and the matching SploitAgent skill loads to work an authorized target from recon to report.">

</div>

---

## What it is

Each skill is a Markdown file (`skills/<domain>/<slug>/SKILL.md`) with a trigger line and a method
(when it applies · why it works · exact commands · gotchas · how to verify). Your agent reads the
trigger, loads the one skill that fits your request, and follows it. No runtime, no lock-in — just
knowledge the agent didn't have.

- **Input:** plain English — *"test this API for access-control bugs."*
- **Output:** the agent runs the technique, proves impact, and writes findings + a report to disk.
- **Guardrail:** it confirms authorization first and refuses anything outside your defined scope.

## Install

**Requirements:** an AI coding agent ([Claude Code](https://claude.com/claude-code) recommended; Codex/Gemini/local also work), `git`, a terminal.

```bash
git clone https://github.com/NoorQureshi/SploitAgent && cd SploitAgent
./sploit install
```

`./sploit install` does two things: links all 127 skills into `~/.claude/skills/` (so Claude Code
finds them in **any** directory) and puts the `sploit` command on your `PATH`. Undo anytime with
`./install.sh --uninstall`.

## Use

```bash
sploit new acme.com ~/work/acme     # 1. make a workspace for the target (put it anywhere)
cd ~/work/acme                      # 2. edit scope.txt with your authorized targets
claude                              # 3. open your agent here (or: codex · gemini)
```

Then type your goal:

```
Start an authorized assessment of acme.com. Confirm scope, then recon.
```

## What it does — example run

The agent confirms scope, then loads skills as the target reveals leads. Abridged session:

```text
> Start an authorized assessment of acme.com. Confirm scope, then recon.

● tradecraft-scope-roe             scope confirmed · *.acme.tld (bug-bounty, in scope)
● recon-subdomain-enum             41 hosts found · api.acme.tld is live
● recon-techstack-fingerprinting   Django REST Framework · Cloudflare WAF · /api/v1
● api-bola                         testing object references on /api/v1/orders
    ✓ GET /api/v1/orders/1044  (account B's token)  → returns account A's order
    ✓ IDs are sequential → ~20k orders enumerable (not hoarded)
● web-idor                         confirmed cross-tenant read with 2 accounts
● reporting-triage-validation      reproduced from a clean session · CVSS 8.1 (High) · not a dup
✔ wrote findings/idor-orders.md
```

**What you get on disk** — the workspace, updated as it works:

```text
~/work/acme/
  scope.txt                 your authorized targets (the hard boundary)
  notes.md                  timestamped log of every step (goal · command · result · why · next)
  findings/idor-orders.md   the confirmed finding, ready to submit
```

`findings/idor-orders.md` looks like this:

```markdown
# IDOR → cross-tenant order access on /api/v1/orders/{id}

Severity: High (CVSS 8.1 — AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N)
Asset:    https://api.acme.tld/api/v1/orders/{id}

## Steps to reproduce
1. Log in as attacker (account B) and capture the bearer token.
2. Request another tenant's order:  GET /api/v1/orders/1044  with B's token.
3. Response returns account A's order (name, address, line items).

## Impact
Any authenticated user can read any other tenant's orders by changing a sequential id
(~20k records enumerable). Cross-tenant confidentiality breach.

## Fix
Enforce object-level authorization: check the order's owner == the caller on every read.
```

That's the whole point: **you describe the task, the agent does the work and hands you evidence.**
See a fully annotated run → **[How it works](https://noorqureshi.github.io/SploitAgent/interact.html)**.

## Common requests

| You type… | The agent loads |
|---|---|
| "recon acme.com and map the attack surface" | `recon-*` |
| "test this API for IDOR / BOLA (I'm authorized)" | `api-bola`, `web-idor` |
| "is this login's JWT forgeable?" | `web-auth-jwt` |
| "review ./src for injection bugs" | `code-review-*` |
| "I got a shell — what now?" | `privesc-enumeration` |
| "kerberoast the domain controller (authorized pentest)" | `ad-kerberoasting` |
| "turn this finding into a report" | `reporting-*` |
| "write a Sigma rule to detect this" | `defense-detection-sigma` |

## What's inside

**127 skills across 20 domains.** [🔎 Search them all](https://noorqureshi.github.io/SploitAgent/catalog.html) · or browse [CATALOG.md](CATALOG.md).

`web` · `api` · `cloud` · `ad` · `network` · `wireless` · `recon` · `mobile` · `ai-ml` ·
`code-review` · `reverse-engineering` · `cryptography` · `exploit-dev` · `privesc` · `payloads` ·
`defense` · `reporting` · `automation` · `tradecraft` · `social-eng`

<details>
<summary><b>See what each domain covers</b></summary>

| Domain | # | Covers |
|---|:--:|---|
| [`web`](skills/web) | 36 | XSS, SQLi, SSRF, SSTI, IDOR, XXE, CSRF, CORS, LFI, deserialization, OAuth, SAML, request smuggling, prototype pollution, cache poisoning, host-header, clickjacking, WebSocket, race conditions, business logic, file upload, JWT, account takeover, dependency confusion, client-side signing reversal, authenticated session handling, Python sandbox escape, Cypher injection, JDBC/connection-string RCE |
| [`ai-ml`](skills/ai-ml) | 9 | Prompt injection, jailbreaks, RAG poisoning, model extraction, agent/tool and MCP abuse, insecure output handling, supply chain, unbounded consumption |
| [`cloud`](skills/cloud) | 9 | IMDS credential theft, object-storage exposure, Kubernetes, container escape, exposed Docker/daemon API abuse, IAM privilege escalation, registries, GCP, Azure / Entra ID |
| [`api`](skills/api) | 8 | BOLA/BFLA, GraphQL, gRPC, mass assignment, authentication attacks, fuzzing, version drift, NoSQL injection |
| [`recon`](skills/recon) | 8 | Subdomain enumeration, DNS analysis, content and JS discovery, OSINT, cloud-asset discovery, service enumeration, tech-stack fingerprinting |
| [`defense`](skills/defense) | 6 | Detection engineering (Sigma/ATT&CK), hardening baselines, DFIR triage, threat modeling, log analysis, purple teaming |
| [`code-review`](skills/code-review) | 6 | Methodology, dangerous-sink catalog, secrets detection, CI/CD security, Python, Node.js |
| [`mobile`](skills/mobile) | 5 | Android and iOS assessment, certificate-pinning bypass, deep-link abuse, WebView abuse |
| [`ad`](skills/ad) | 5 | Kerberoasting / AS-REP, ADCS (ESC1–8), ACL/DACL abuse, Kerberos delegation abuse (RBCD / S4U / coercion→relay), pivoting arsenal |
| [`network`](skills/network) | 6 | Service attacks, pivoting and tunneling, NTLM coercion and relay, password spraying and credential stuffing, perimeter appliance and VPN offensive, hash and credential cracking |
| [`wireless`](skills/wireless) | 2 | WPA2-PSK handshake/PMKID capture and cracking, evil-twin / rogue-AP enterprise (PEAP-MSCHAPv2) credential harvesting |
| [`privesc`](skills/privesc) | 4 | Post-foothold enumeration and credential hunting, Linux arsenal, GTFOBins (sudo/SUID/capabilities), Windows token impersonation |
| [`exploit-dev`](skills/exploit-dev) | 3 | Exploit chaining and impact amplification, PoC development, memory-corruption exploitation (ROP / format string / ret2libc) |
| [`reverse-engineering`](skills/reverse-engineering) | 3 | Native binary triage, deobfuscation (packed/JS/WASM/JSVMP), firmware extraction and analysis |
| [`cryptography`](skills/cryptography) | 2 | Weak/textbook RSA (JWT RS256, custom signatures), symmetric oracles (CBC padding, ECB, hash length extension) |
| [`payloads`](skills/payloads) | 4 | WAF/filter bypass, XSS polyglots, reverse shells and TTY upgrade, file transfers |
| [`reporting`](skills/reporting) | 3 | Finding triage and validation, bug-bounty write-up, penetration-test report |
| [`automation`](skills/automation) | 2 | Recon pipelines, custom nuclei templates |
| [`tradecraft`](skills/tradecraft) | 2 | Scope and rules of engagement, complex multi-stage engagements |
| [`social-eng`](skills/social-eng) | 4 | Authorized human-factor testing: methodology, phishing, vishing/pretexting, physical assessment (pentest-only) |

</details>

## FAQ

<details>
<summary><b>Do I need to install security tools?</b></summary>

The skills are the *method* and name the standard tools each step uses (nmap, ffuf, sqlmap, impacket…).
Install what a given skill calls for when you need it; the agent runs them in your terminal.
</details>

<details>
<summary><b>Which agents work, and does the workspace have to be in this repo?</b></summary>

Claude Code works best (it auto-loads the matching skill). Codex, Gemini, and local models work too —
they read `AGENTS.md` and the skill files. Workspaces can live **anywhere**: `sploit new <target> <path>`
wires the skills in; add `--copy` to make the folder fully standalone.
</details>

<details>
<summary><b>Will it attack things on its own?</b></summary>

No. The first skill in every engagement, `tradecraft-scope-roe`, makes the agent confirm authorization
and refuse anything not in your `scope.txt`. You stay in control.
</details>

## Authorized use only

For security work you're **permitted** to do — a signed pentest scope, a bug-bounty program that lists
the target, or systems you own. Don't point it at anything you aren't authorized to test.

## Contribute

A contribution is a single Markdown file — no code:

```bash
cp skills/_templates/technique.md skills/<domain>/<slug>/SKILL.md
python3 tools/catalog.py            # validate + regenerate the indexes
```

Wanted skills: [ROADMAP.md](ROADMAP.md) · full guide: [CONTRIBUTING.md](CONTRIBUTING.md). Every PR is schema-validated by CI.

## Repository layout

```text
sploit                            front door: new <target> [dir] · install · list
install.sh                        link skills into ~/.claude/skills (Claude Code)
skills/<domain>/<slug>/SKILL.md   the library
AGENTS.md · CLAUDE.md             operating guide read by any in-repo agent
methodology.md                    engagement loop, scope rule, note-taking standard
tools/catalog.py                  validation + index generation (schema in schemas/)
CATALOG.md · COVERAGE.md          generated indexes
docs/                             usage guide and project site
```

## License

[MIT](LICENSE). Built for authorized security work.
