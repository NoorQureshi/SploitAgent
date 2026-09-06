<h1 align="center">🥷 Ronin</h1>

<p align="center">
  <b>The open library of hacking skills for AI agents.</b><br>
  Load it into your agent and it works like a senior operator — recon to report, offense and defense.
</p>

<p align="center">
  <a href="https://github.com/NoorQureshi/ronin/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/NoorQureshi/ronin/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="skills" src="https://img.shields.io/badge/skills-61-6E56CF">
  <img alt="domains" src="https://img.shields.io/badge/domains-16-6E56CF">
  <img alt="for" src="https://img.shields.io/badge/for-pentest_·_bug_bounty_·_defense-0b7285">
  <img alt="scope" src="https://img.shields.io/badge/use-authorized_only-red">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-blue">
</p>

---

**Ronin is not a tool — it's a library.** It's the knowledge of *how to actually do the work* —
find the bug, prove the impact, escalate, pivot, report, and defend — written as small,
trigger-tagged **skills** in the standard Agent-Skills format. Point any AI agent (Claude Code,
Codex, Gemini, a local model) at the `skills/` folder and it loads the right skill automatically
for the task in front of it.

It's built for the people who do this for a living or for sport-with-permission:

- **Penetration testers** — a full engagement method plus tool arsenals and concrete chains.
- **Bug-bounty hunters** — the web/API/mobile/cloud/LLM classes that actually pay, with triage-ready reporting.
- **Defenders** — the other half: detection engineering, hardening, and DFIR, mapped to the same attacks.

No runtime, no lock-in. The skills are plain Markdown you can read, grep, copy, and improve.

## Why a library, not a tool

Tools go stale; knowledge compounds. A scanner encodes one team's checks at one moment. A
*library of skills* encodes **how to think** — the mechanism behind each bug, the exact command
with the flag that matters, the gotcha that tells "not vulnerable" apart from "you did it wrong."
Agents change every quarter; the tradecraft doesn't. Keep it in one place, in the open, and every
agent that loads it gets sharper — and so does every contributor who reads it.

Each skill is written to **teach the mechanism**, not just paste a payload:

> *when it applies · why it works · method (exact commands + flag gloss) · gotchas · verify success*

## What's inside — 61 skills across 16 domains

| Domain | Skills | Covers |
|---|--:|---|
| **web** | 21 | XSS, SQLi, SSRF, SSTI, IDOR, JWT, upload, XXE, CSRF, CORS, LFI, request-smuggling, deserialization, OAuth, subdomain-takeover, business-logic, race-conditions… |
| **api** | 6 | BOLA/BFLA, mass assignment, GraphQL, auth attacks, fuzzing, NoSQL injection |
| **recon** | 5 | subdomain enum, content/JS discovery, OSINT, service enum, the tooling arsenal |
| **cloud** | 4 | IMDS/SSRF → creds, S3/bucket exposure, Kubernetes, container escape |
| **ai-ml** | 3 | prompt injection, jailbreaks, RAG/knowledge-base poisoning |
| **defense** | 3 | detection engineering (Sigma/ATT&CK), hardening baselines, DFIR triage |
| **code-review** | 3 | review methodology, dangerous-sink catalog, secrets detection |
| **mobile** | 3 | Android assessment, cert-pinning bypass, deep-link/intent abuse |
| **network** | 2 | non-web service attacks, pivoting & tunneling |
| **exploit-dev** | 2 | exploit chaining & impact amplification, PoC development |
| **payloads** | 2 | WAF/filter bypass, XSS polyglots (with reference payload sets) |
| **automation** | 2 | recon pipelines, custom nuclei templates |
| **tradecraft** | 2 | scope & rules-of-engagement, complex multi-stage engagements |
| **ad · privesc · reporting** | 3 | Active Directory & pivoting, Linux/Windows privesc, bug-bounty reporting |

Browse the full, always-current list in **[`CATALOG.md`](CATALOG.md)**. Every skill carries
OWASP / OWASP-LLM / OWASP-API / MITRE ATT&CK / CWE tags in its frontmatter, so coverage is
measurable and gaps are visible.

## Use it in 30 seconds

```bash
git clone https://github.com/noorqureshi/ronin
# Claude Code: expose the skills to your agent
ln -s "$PWD/ronin/skills" ~/.claude/skills/ronin      # or: cp -r ronin/skills/* ~/.claude/skills/
```

Then just describe an **authorized** target and let the agent pick the skills:

> *"Bug-bounty program acme.com, wildcard in scope. Start recon, then hunt the API."*

Works the same with Codex, Gemini, or a local model — point the agent at `skills/`, or drop a
specific `SKILL.md` into context. Details for each: **[docs/USING.md](docs/USING.md)**.

## The rule that comes first

> ⚠️ **Authorized use only.** The first skill every engagement loads is `tradecraft-scope-roe`.
> Ronin operates only inside a confirmed **authorization envelope** — a signed pentest scope, a
> bug-bounty program you're in scope for, or systems you own/are authorized to test. Out-of-scope
> is a hard block. Never point these skills at anything you don't have permission to test.

## Layout

```
skills/<domain>/<slug>/SKILL.md   ← the library (the point of the repo)
  _templates/                       per-type skill templates
methodology.md                    the engagement loop · scope rule · note-taking standard
schemas/skill.schema.json         the validated skill contract (versioned)
tools/catalog.py                  validate skills + (re)generate CATALOG.md
CATALOG.md                        generated, browsable index of every skill
docs/USING.md                     how to load Ronin into each AI agent
CONTRIBUTING.md                   how to add a skill
```

## Contributing

New skills are the whole point — especially techniques you've proven on real (authorized) targets
and defensive counterparts to the attacks. It's Markdown, not code:

```bash
cp skills/_templates/technique.md skills/<domain>/<slug>/SKILL.md
# write it, then:
python3 tools/catalog.py validate    # schema-check
python3 tools/catalog.py             # regenerate CATALOG.md
```

Strong trigger keywords, teach the mechanism, no real targets/creds. Full guide and PR checklist:
**[CONTRIBUTING.md](CONTRIBUTING.md)**. CI validates every skill against the schema on each push.

## License

MIT — see [LICENSE](LICENSE). Use it responsibly and legally.
