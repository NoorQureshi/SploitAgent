<div align="center">

# SploitAgent

**Security skills for AI agents.**
Turn Claude Code (or any AI agent) into a capable security operator — 127 ready-to-use skills, offensive and defensive, for **authorized** pentesting, bug-bounty, and blue-team work.

[![CI](https://github.com/NoorQureshi/SploitAgent/actions/workflows/ci.yml/badge.svg)](https://github.com/NoorQureshi/SploitAgent/actions/workflows/ci.yml)
![skills](https://img.shields.io/badge/skills-127-334155?style=flat-square)
![domains](https://img.shields.io/badge/domains-20-334155?style=flat-square)
![mapped](https://img.shields.io/badge/mapped-OWASP%20%C2%B7%20MITRE%20ATT%26CK-334155?style=flat-square)
![license](https://img.shields.io/badge/license-MIT-334155?style=flat-square)

<sub>[Docs & site](https://noorqureshi.github.io/SploitAgent/) · [How it works](https://noorqureshi.github.io/SploitAgent/interact.html) · [Search skills](https://noorqureshi.github.io/SploitAgent/catalog.html) · [Contributing](CONTRIBUTING.md)</sub>

<img src="docs/terminal.svg" width="820" alt="A Claude Code terminal session: describe a task in plain English and the matching SploitAgent skill loads to work an authorized target from recon to report.">

</div>

---

## The idea in one line

Your AI agent is smart, but it doesn't *know security*. **SploitAgent is that missing knowledge** — a
library of proven techniques your agent pulls up exactly when a task needs them. Think of it as handing
your agent a senior pentester's playbook.

## What you get

- **Just describe the task.** Nothing to memorize. Say *"test this API for access-control bugs"* and the
  agent loads the right skill and follows its method.
- **127 skills across 20 domains** — web, API, cloud, Active Directory, mobile, crypto, reversing, recon,
  reporting, defense, and more (full list [below](#whats-inside)).
- **Works with your agent.** Claude Code, Codex, Gemini, or a local model. It's plain Markdown — no
  runtime, nothing to build, no lock-in.
- **Safe by design.** Every engagement confirms you're authorized first and refuses anything out of scope.

## Before you start

You'll need three things:

1. **An AI coding agent** — [Claude Code](https://claude.com/claude-code) (recommended), or Codex / Gemini / a local model.
2. **`git`** and a terminal.
3. **A target you're allowed to test** — your own app, a signed pentest engagement, or a bug-bounty program that lists it in scope.

## Get started — 3 steps

```bash
# 1) Install once — makes the skills available to Claude Code everywhere
git clone https://github.com/NoorQureshi/SploitAgent && cd SploitAgent
./sploit install

# 2) Create a workspace for your target — put it anywhere you like
sploit new acme.com ~/work/acme

# 3) Open your agent in that folder
cd ~/work/acme && claude          # or: codex · gemini
```

Now just tell it what you want, in plain English:

> **"Start an authorized assessment of acme.com. Confirm scope, then recon."**

The agent reads your `scope.txt`, loads the matching skills, and gets to work.
Want to watch a full run first? → **[How it works](https://noorqureshi.github.io/SploitAgent/interact.html)**

## Just talk to it — examples

| You type… | The agent loads |
|---|---|
| "recon acme.com and map the attack surface" | `recon-*` |
| "test this API for IDOR / BOLA (I'm authorized)" | `api-bola`, `web-idor` |
| "is this login's JWT forgeable?" | `web-auth-jwt` |
| "review ./src for injection bugs before we ship" | `code-review-*` |
| "I got a shell — what now?" | `privesc-enumeration` |
| "kerberoast the domain controller (authorized pentest)" | `ad-kerberoasting` |
| "turn this finding into a report" | `reporting-*` |
| "write a Sigma rule to detect this" | `defense-detection-sigma` |

## What happens under the hood

The agent always follows the same simple loop — the target decides which skills fire at each step:

1. **Scope** — confirm you're authorized · `tradecraft-scope-roe`
2. **Recon** — map the target · `recon-*`
3. **Attack** — by area: web · API · cloud · AD · wireless… · `web-*`, `api-*`, `cloud-*`, …
4. **Escalate & pivot** — go deeper · `privesc-*`, `ad-*`, `network-*`
5. **Report** — validate, then write it up · `reporting-*`
6. **Defend** *(optional)* — turn findings into detections · `defense-*`

Everything for one target lives in its own folder (`sploit new` creates it — **anywhere**, with the
skills wired in, so any agent opened there can use them):

```
<your target folder>/
  scope.txt  roe.md  notes.md  findings/  loot/  START-HERE.md
  skills/   CLAUDE.md   AGENTS.md
```

<a id="whats-inside"></a>

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
<summary><b>Do I need to install a bunch of security tools?</b></summary>

No — the skills are *knowledge*, not the tools themselves. They teach the method and name the standard
tools each step uses (nmap, ffuf, sqlmap, etc.). Install whatever a given skill calls for, when you
need it. Many skills need nothing beyond what the agent already has.
</details>

<details>
<summary><b>Which agents work?</b></summary>

Claude Code works best (it auto-loads the right skill). Codex, Gemini, and other agents work too — they
read `AGENTS.md` and the skill files. Local models work as well; see [docs/USING.md](docs/USING.md).
</details>

<details>
<summary><b>Will it attack things on its own?</b></summary>

No. Every engagement starts with `tradecraft-scope-roe`, which makes the agent confirm authorization
and refuse anything not in your `scope.txt`. You stay in control.
</details>

<details>
<summary><b>Does the workspace have to be inside this repo?</b></summary>

No — `sploit new <target> <path>` puts it wherever you want and wires the skills in. Add `--copy` to
make it fully standalone (it keeps working even if you move or delete the repo).
</details>

<details>
<summary><b>How do I update it?</b></summary>

`git pull` in the repo. If you ran `./sploit install`, re-run it to refresh the links.
</details>

## Authorized use only

SploitAgent is for security work you're **permitted** to do: a signed pentest scope, a bug-bounty
program whose scope covers the target, or systems you own. The first skill in every engagement,
`tradecraft-scope-roe`, requires an explicit authorization before anything runs. Don't point it at
systems you aren't authorized to test.

## Contribute

A contribution is a single Markdown file — no code:

```bash
cp skills/_templates/technique.md skills/<domain>/<slug>/SKILL.md
python3 tools/catalog.py            # validate + regenerate the indexes
```

Wanted skills are in [ROADMAP.md](ROADMAP.md); the full guide and house style are in
[CONTRIBUTING.md](CONTRIBUTING.md). Every pull request is schema-validated by CI.

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
