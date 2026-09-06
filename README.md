<div align="center">

# 🥷 Ronin

**The open library of hacking skills for AI agents.**

Point any AI agent at Ronin and it works like a seasoned operator — recon to report, offense and defense.

[![CI](https://github.com/NoorQureshi/ronin/actions/workflows/ci.yml/badge.svg)](https://github.com/NoorQureshi/ronin/actions/workflows/ci.yml)
![skills](https://img.shields.io/badge/skills-85-6E56CF)
![domains](https://img.shields.io/badge/domains-16-6E56CF)
![for](https://img.shields.io/badge/for-pentest_·_bug_bounty_·_defense-0b7285)
![use](https://img.shields.io/badge/use-authorized_only-red)
![license](https://img.shields.io/badge/license-MIT-blue)

[**Use it**](#use-it-with-any-agent) · [Domains](#the-16-domains) · [Catalog](CATALOG.md) · [Coverage](COVERAGE.md) · [Contribute](CONTRIBUTING.md) · [Roadmap](ROADMAP.md)

</div>

---

Ronin is **not a tool — it's a library.** It captures *how the work is actually done* — find the
bug, prove the impact, escalate, pivot, report, and defend — as small, trigger-tagged **skills** in
the standard Agent-Skills format. Drop it in front of any AI agent and the right skill loads itself
for the task at hand.

```text
you:   "Bug-bounty program acme.com, wildcard in scope. Map it, then hunt the API."
agent: loads tradecraft-scope-roe → recon-subdomain-enum → recon-content-discovery → api-fuzzing → api-bola …
```

## Use it with any agent

The skills are plain Markdown, so any agent can use them. Pick your setup:

<details open>
<summary><b>Claude Code</b></summary>

**Option A — open Claude Code inside the repo (zero setup).** It reads `CLAUDE.md`, which teaches it
how to use the skills and to confirm scope first.
```bash
git clone https://github.com/NoorQureshi/ronin && cd ronin
claude          # then: "Here's my authorized target … start recon"
```

**Option B — make the skills available in every project.** Symlink them into your user scope once:
```bash
git clone https://github.com/NoorQureshi/ronin
ln -s "$PWD/ronin/skills" ~/.claude/skills/ronin
```
</details>

<details>
<summary><b>Codex, Gemini & other agents</b></summary>

Clone the repo and open your agent in it — it reads **`AGENTS.md`** (the same operating guide),
or point the agent at the `skills/` folder. For a one-off, paste a single `SKILL.md` into context.
```bash
git clone https://github.com/NoorQureshi/ronin && cd ronin
```
</details>

<details>
<summary><b>Any other / open-source agent</b></summary>

There's no runtime to install. Give the agent read access to `skills/` (and `AGENTS.md` for the
operating guide), or load the specific `SKILL.md` for the task. That's it.
</details>

> [!WARNING]
> **Authorized use only.** The first skill every engagement loads is **`tradecraft-scope-roe`** —
> Ronin acts only inside a confirmed envelope: a signed pentest scope, a bug-bounty program you're
> in scope for, or systems you own. Never point it at anything else.

## How an agent works a target

Ronin gives the agent a repeatable loop and a place to keep its work — so runs are consistent
whether it's Claude Code, Codex, or an open-source agent. (Full method: [`methodology.md`](methodology.md);
agent guide: [`AGENTS.md`](AGENTS.md).)

```
1. Scope      confirm authorization, write scope.txt      → tradecraft-scope-roe
2. Recon      map the surface                             → recon-*
3. Attack     route by domain (web/api/cloud/mobile/ad…)  → web-*, api-*, cloud-* …
4. Foothold   prove impact, chain bugs                    → exploit-chaining
5. Escalate   privesc + lateral movement                  → privesc-*, ad-*, network-*
6. Report     findings with severity + evidence           → reporting-*
7. Defend     turn findings into detections               → defense-*
```

Each engagement gets its own workspace (all git-ignored, so it never pollutes the repo):

```
engagements/<target>/
  scope.txt   roe.md   notes.md   findings/   loot/
```

## The 16 domains

**85 skills.** Every skill is one `SKILL.md`; the full list is in **[CATALOG.md](CATALOG.md)**.

| Domain | Skills | What it covers |
|---|:--:|---|
| [`web`](skills/web) | 29 | XSS · SQLi · SSRF · SSTI · IDOR · XXE · CSRF · CORS · LFI · deserialization · OAuth · request smuggling · prototype pollution · cache poisoning · host-header · clickjacking · websocket · race conditions · business logic · upload · JWT · account takeover |
| [`api`](skills/api) | 8 | BOLA/BFLA · GraphQL · gRPC · mass assignment · auth attacks · fuzzing · versioning · NoSQL injection |
| [`recon`](skills/recon) | 7 | subdomain enum · DNS analysis · content & JS discovery · OSINT · cloud-asset discovery · service enumeration |
| [`ai-ml`](skills/ai-ml) | 6 | prompt injection · jailbreaks · RAG poisoning · model extraction · agent/tool abuse · LLM denial-of-wallet |
| [`cloud`](skills/cloud) | 6 | IMDS→credential theft · S3/bucket exposure · Kubernetes · container escape · IAM privesc · container registries |
| [`mobile`](skills/mobile) | 5 | Android & iOS assessment · cert-pinning bypass · deep-link abuse · WebView abuse |
| [`code-review`](skills/code-review) | 4 | review methodology · dangerous-sink catalog · secrets detection · CI/CD pipeline security |
| [`defense`](skills/defense) | 4 | detection engineering (Sigma/ATT&CK) · hardening baselines · DFIR triage · threat modeling |
| [`ad`](skills/ad) | 2 | Kerberoasting / AS-REP · Active Directory & pivoting arsenal |
| [`network`](skills/network) | 2 | non-web service attacks · pivoting & tunneling |
| [`exploit-dev`](skills/exploit-dev) | 2 | exploit chaining & impact amplification · PoC development |
| [`privesc`](skills/privesc) | 2 | Linux/Windows arsenal · GTFOBins (sudo/SUID/capabilities) |
| [`payloads`](skills/payloads) | 2 | WAF/filter bypass · XSS polyglots |
| [`reporting`](skills/reporting) | 2 | bug-bounty write-up · full pentest report |
| [`automation`](skills/automation) | 2 | recon pipelines · custom nuclei templates |
| [`tradecraft`](skills/tradecraft) | 2 | scope & rules-of-engagement · complex multi-stage engagements |

Every skill carries OWASP / OWASP-LLM / OWASP-API / MITRE ATT&CK / CWE tags — see **[COVERAGE.md](COVERAGE.md)**.

## What a skill looks like

A trigger line (so the agent knows *when* to load it) and a body that teaches the *mechanism*:

```markdown
---
name: web-ssrf
description: Discover and escalate Server-Side Request Forgery. Load when the app
  fetches a URL you influence: webhooks, "import from URL", PDF/image render…
domain: web
type: technique
modes: [pentest, bugbounty]
owasp: [A10:2021-SSRF]
cwe: [CWE-918]
---
## When it applies · Why it works · Method (exact commands + flag gloss) · Gotchas · Verify success
```

That shape is the house style — useful to a human *and* an agent.

## Why Ronin

- **Knowledge outlasts tools.** A library of skills encodes *how to think* — the mechanism, the
  exact command, the gotcha. Agents change every quarter; the tradecraft doesn't.
- **Portable, no lock-in.** Plain Markdown, standard Agent-Skills format. No runtime, no build step.
- **Offense *and* defense.** Every attack has its counterpart — detection, hardening, DFIR.
- **Built to grow.** A schema keeps every skill consistent; a contribution is one Markdown file.

## Contribute

Ronin gets sharper with every skill added — and adding one is a single Markdown file, no code:

```bash
cp skills/_templates/technique.md skills/<domain>/<slug>/SKILL.md
python3 tools/catalog.py            # validate + regenerate the indexes
```

New to it? The **[Roadmap](ROADMAP.md)** lists wanted skills (🟢 = good first one). Full guide and
PR checklist in **[CONTRIBUTING.md](CONTRIBUTING.md)**; CI schema-validates every PR.

## Layout

```text
skills/<domain>/<slug>/SKILL.md   the library (the point of the repo)
AGENTS.md · CLAUDE.md             operating guide any agent reads in-repo
methodology.md                    the engagement loop · scope rule · note standard
schemas/skill.schema.json         the skill contract (validated in CI)
tools/catalog.py                  validate skills + regenerate CATALOG.md / COVERAGE.md
CATALOG.md · COVERAGE.md          generated indexes
docs/USING.md · CONTRIBUTING.md · ROADMAP.md
```

## License

MIT — see [LICENSE](LICENSE). Built for people who do this legally and with permission.
