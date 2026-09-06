<div align="center">

# 🥷 Ronin

**The open library of hacking skills for AI agents.**

Point your agent at Ronin and it works like a seasoned operator — recon to report, offense and defense.

[![CI](https://github.com/NoorQureshi/ronin/actions/workflows/ci.yml/badge.svg)](https://github.com/NoorQureshi/ronin/actions/workflows/ci.yml)
![skills](https://img.shields.io/badge/skills-85-6E56CF)
![domains](https://img.shields.io/badge/domains-16-6E56CF)
![for](https://img.shields.io/badge/for-pentest_·_bug_bounty_·_defense-0b7285)
![use](https://img.shields.io/badge/use-authorized_only-red)
![license](https://img.shields.io/badge/license-MIT-blue)

[Browse the catalog](CATALOG.md) · [Coverage](COVERAGE.md) · [Using Ronin](docs/USING.md) · [Contribute](CONTRIBUTING.md) · [Roadmap](ROADMAP.md)

</div>

---

Ronin is **not a tool — it's a library.** It's the knowledge of *how the work is actually done* —
find the bug, prove the impact, escalate, pivot, report, and defend — written as small,
trigger-tagged **skills**. Drop it in front of any AI agent (Claude Code, Codex, Gemini, a local
model) and the right skill loads itself for the task in front of it.

```text
you:   "Bug-bounty program acme.com, wildcard in scope. Map it, then hunt the API."
agent: loads recon-subdomain-enum → recon-content-discovery → api-fuzzing → api-bola …
```

## Why Ronin

- **Knowledge outlasts tools.** Scanners encode one team's checks at one moment; a library of
  skills encodes *how to think* — the mechanism, the exact command, the gotcha. Agents change
  every quarter; the tradecraft doesn't.
- **Portable, no lock-in.** Plain Markdown in the standard Agent-Skills format. No runtime, no
  build step, no framework to adopt. Read it, grep it, copy it, improve it.
- **Offense *and* defense.** Every attack has its counterpart — detection, hardening, DFIR — so
  the same library serves red and blue.
- **Built to grow.** A schema keeps every skill consistent; contributions are one Markdown file.

## What's inside

**85 skills across 16 domains.** Full, always-current list in **[CATALOG.md](CATALOG.md)**.

| Domain | | Domain | | Domain | |
|---|--:|---|--:|---|--:|
| `web` | 29 | `cloud` | 6 | `code-review` | 4 |
| `api` | 8 | `ai-ml` | 6 | `mobile` | 5 |
| `recon` | 7 | `defense` | 4 | `ad` · `network` · `exploit-dev` · `privesc` · `payloads` · `automation` · `reporting` · `tradecraft` | 2 each |

Every skill carries OWASP / OWASP-LLM / OWASP-API / MITRE ATT&CK / CWE tags, so coverage is
measurable and gaps are visible — see **[COVERAGE.md](COVERAGE.md)**.

## What a skill looks like

Each `SKILL.md` has a trigger line (so the agent knows *when* to load it) and a body that teaches
the *mechanism*, not just a payload:

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

That shape — *when it applies · why it works · method · gotchas · verify* — is the house style,
and it's what makes the skills useful to a human *and* an agent.

## Quickstart

```bash
git clone https://github.com/noorqureshi/ronin

# Claude Code — expose the skills to your agent:
ln -s "$PWD/ronin/skills" ~/.claude/skills/ronin      # or: cp -r ronin/skills/* ~/.claude/skills/
```

Then describe an **authorized** target and let the agent pick the skills. Codex, Gemini, and local
models work the same way — point them at `skills/`, or drop a single `SKILL.md` into context.
Full instructions per agent: **[docs/USING.md](docs/USING.md)**.

> [!WARNING]
> **Authorized use only.** The first skill every engagement loads is `tradecraft-scope-roe`.
> Ronin operates only inside a confirmed authorization envelope — a signed pentest scope, a
> bug-bounty program you're in scope for, or systems you own. Never point it at anything else.

## Contribute — this is the point

Ronin gets sharper with every skill added, and adding one is deliberately easy: **it's a single
Markdown file, no code.**

```bash
cp skills/_templates/technique.md skills/<domain>/<slug>/SKILL.md
# write it, then:
python3 tools/catalog.py            # validate + regenerate the catalog
```

- **Not sure what to write?** The **[Roadmap](ROADMAP.md)** lists wanted skills — the 🟢 ones are
  great first contributions.
- **Have a technique you've used on a real (authorized) target?** That's exactly what belongs here.
- **Blue team?** Detection, hardening, and DFIR skills are just as welcome as offensive ones.

Full guide, house style, and PR checklist: **[CONTRIBUTING.md](CONTRIBUTING.md)**. Every PR is
schema-validated by CI, so it's hard to get the format wrong.

## Layout

```text
skills/<domain>/<slug>/SKILL.md   the library (the point of the repo)
methodology.md                    the engagement loop · scope rule · note standard
schemas/skill.schema.json         the skill contract (validated in CI)
tools/catalog.py                  validate skills + regenerate CATALOG.md / COVERAGE.md
CATALOG.md · COVERAGE.md          generated indexes
docs/USING.md · CONTRIBUTING.md · ROADMAP.md
```

## License

MIT — see [LICENSE](LICENSE). Built for people who do this legally and with permission.
