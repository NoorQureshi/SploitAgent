<h1 align="center">🥷 Ronin</h1>

<p align="center">
  <b>The open library of hacking skills for AI agents — authorized CTF, bug bounty & defense.</b><br>
  One curated skill set. Load it into <b>Claude Code</b>, <b>Codex</b>, <b>Gemini CLI</b>, or a <b>local model</b>.
</p>

<p align="center">
  <a href="https://github.com/NoorQureshi/ronin/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/NoorQureshi/ronin/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="library" src="https://img.shields.io/badge/library-60%2B_skills_·_16_domains-6E56CF">
  <img alt="scope" src="https://img.shields.io/badge/scope-authorized_use_only-red">
  <img alt="works with" src="https://img.shields.io/badge/works_with-Claude_·_Codex_·_Gemini_·_local-6E56CF">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-blue">
</p>

---

A ronin serves no single master and fights with whatever weapon is at hand. Ronin is the same:
**not a tool — a library.** It's the *knowledge* of how to hack, written as trigger-loaded
**skills** an AI agent picks up automatically for the task in front of it — recon, web, API,
mobile, cloud, Active Directory, LLM/AI, source-code review, privesc, plus the defensive,
reporting, and tradecraft craft. A full engagement methodology and a growing, curated skill set,
kept in **one tool-neutral core** and compiled for **whatever AI CLI you already run**. An
optional `ronin` CLI helps you install tooling and scaffold work — but the skills are the point,
and adding to them is meant to be easy.

> ⚠️ **Authorized use only.** Scope discipline is the first instruction in every component:
> Ronin refuses to act until the target is inside a confirmed **authorization envelope** — a
> lab range (HackTheBox / TryHackMe / Pro Labs / CPTS-OSCP) **or** a bug-bounty program you are
> in-scope for, within its rules of engagement. Never point it at anything you don't own or
> aren't explicitly authorized to test.

## How it works

The valuable part — *how to think through a target* — is portable knowledge. Ronin keeps the
skills in **one source of truth** and generates each AI tool's entry file from it, so nothing is
written twice and nothing drifts. Contributors add skills; every agent that loads Ronin gets sharper.

```
ronin                         ← optional CLI: doctor · install · build · validate · catalog · start · local · new · lock
setup.sh                      ← one-time bootstrap (build + put `ronin` on PATH)
framework/                    ← SINGLE SOURCE OF TRUTH
  methodology.md                the loop · scope rule · note-taking standard          🔒 locked
  roles/                        phase playbooks: recon·web·ad·privesc·report·learn     🔒 locked
  skills/<domain>/<slug>/       skills by domain — recon web api mobile cloud network
                                ad ai-ml code-review exploit-dev privesc defense
                                payloads reporting automation tradecraft
    SKILL.md                      arsenal · technique · methodology · checklist · reference
                                  each tagged stability (🔒 locked / ✍️ learning) + modes
  _templates/                   per-type skill templates
schemas/skill.schema.json       the validated skill contract (versioned)
adapters/
  build.sh                      generator → per-tool entry files + catalog + symlinks
  gen_index.py                  skills indexer: validate · catalog · discovery symlinks
  local/ronin-advisor.py        offline advisor for Ollama / LM Studio
bin/lock.sh · bin/unlock.sh     freeze / deliberately edit the locked core
docs/                           SETUP · HOW-TO-CTF · LOCAL-MODELS
CATALOG.md                      generated, browsable index of every skill
CLAUDE.md   .claude/          ← Claude Code   (full multi-agent: subagents + Skill tool)
AGENTS.md                     ← Codex, Cursor, Zed & other AGENTS.md-aware tools
GEMINI.md                     ← Gemini CLI
```

## Quickstart

```bash
git clone https://github.com/noorqureshi/ronin && cd ronin
./setup.sh                 # build entry files + put `ronin` on your PATH
ronin doctor               # what AI backends & pentest tools you have
ronin install              # install the pentest tools your OS is missing
ronin start claude         # launch in the repo — or: codex | gemini
#   ronin local --provider ollama --model qwen2.5-coder:14b   # fully offline
```

`ronin start` drops you into your agent in the repo. Hand it a **confirmed-authorized** target:

> *"Let's work an HTB box, target 10.129.x.x — it's my authorized lab."*

Ronin confirms scope, scaffolds the engagement directory, and drives the loop —
recon → web/services → foothold → privesc → report — consulting its skills as it goes.

| Your tool | Reads | What you get |
|---|---|---|
| **Claude Code** | `CLAUDE.md` + `.claude/` | Full orchestration — parallel phase **subagents** + the Skill tool |
| **Codex CLI** | `AGENTS.md` | One agent that runs the loop, adopts each phase role, reads the skills |
| **Gemini CLI** | `GEMINI.md` | Same single-agent playbook as Codex |
| **Local LLM** | point any of the above tools at your local model | Same brain, fully offline |

> **Honest scope:** true parallel sub-agents are a **Claude Code** feature. In Codex / Gemini
> / local you get *one strong agent with the complete playbook and tool arsenal* — sharp, but
> sequential. Multi-agent for every backend (incl. local) is the job of the optional runtime
> engine on the roadmap.

### Fully offline (Ollama / LM Studio)

Two ways to run on a **local model**, no cloud:
- **Codex → local endpoint** — point Codex at Ollama (`codex --oss -m qwen2.5-coder:14b`) or
  LM Studio; it reads `AGENTS.md` and runs tools like normal.
- **Built-in advisor** — `python3 adapters/local/ronin-advisor.py --provider ollama --model <m>`:
  a zero-dependency offline coach that loads the framework and walks you through the box.

Full details + model picks → **[docs/LOCAL-MODELS.md](docs/LOCAL-MODELS.md)**.

## The `ronin` command (optional helper)

The skills are the product and work without any CLI. `ronin` is just a convenience layer —
`ronin --help` and `ronin <cmd> --help` everywhere:

| Command | What it does |
|---|---|
| `ronin doctor` | Detect your OS + list which AI backends and pentest tools are installed |
| `ronin install [--group recon\|web\|ad] [--yes]` | Install the missing tools via your OS package manager (apt/brew/pacman/dnf), with pipx/go fallbacks |
| `ronin start claude\|codex\|gemini [--auto]` | Launch that AI backend in the repo. `--auto` skips per-command approvals for hands-off box runs — maps to each tool's YOLO flag (`--dangerously-skip-permissions` / bypass / `--yolo`). **Authorized labs only; VPN in first.** |
| `ronin local --provider ollama\|lmstudio --model <m>` | Start the offline advisor against a local model |
| `ronin new <box> --target <ip>` | Scaffold an engagement dir (`scope.txt`, `notes.md`, `state.md`, `recon/` …) |
| `ronin build [all\|claude-code\|codex\|gemini]` | Regenerate the entry files after editing `framework/` |
| `ronin validate` | Schema-check every skill's frontmatter (domain, type, modes, mappings) |
| `ronin catalog` | Regenerate `CATALOG.md`, the machine index, and discovery symlinks |
| `ronin lock` / `ronin unlock` | Freeze / edit the stable core |

`ronin install` reads what `ronin doctor` found missing and installs it the right way for
your system — no hand-copying setup commands.

## See it in action

`ronin doctor` tells you exactly what your box is missing before you start:

```text
Ronin doctor  ·  Linux x86_64  ·  package manager: apt

AI backends
  ✓ claude   Claude Code (full multi-agent)
  ✗ codex    Codex CLI
  ✗ gemini   Gemini CLI
  ✗ ollama   Ollama (local models)

recon tools
  ✓ nmap                   port/service scanner
  ✗ gobuster               dir/dns/vhost brute
  ✓ ffuf                   web fuzzer
  ...
web tools
  ✗ nuclei                 template vuln scanner
  ✗ katana                 crawler
  ...
7 tool(s) missing.  Install them with:  ronin install
```

## It sharpens itself

When a box or program teaches a reusable trick, the **learn** role captures it as a new
`learning` skill under the right domain (`framework/skills/<domain>/<slug>/SKILL.md`); the
catalog regenerates — so the next target with the same signal auto-applies it. A few of the
techniques already forged from real work:

- **`web-ssrf-gopher-redis-rce`** — SSRF → internal Redis → RCE via `gopher://`.
- **`api-mongo-agg-facet-bypass`** — MongoDB aggregation stage-allowlist bypass via
  `$facet` → `$unionWith` to read sibling collections.
- **`web-webauthn-software-authenticator`** — register/log in to a WebAuthn RP with a
  self-built software authenticator when attestation is `none`.

Edit anything under `framework/`, then re-run `ronin build` (or `./adapters/build.sh all`) to
refresh every tool. Browse the whole library in **[`CATALOG.md`](CATALOG.md)**.

## Locked core vs learning library

The framework improves without ever corrupting what makes it reliable — it's split in two:

- 🔒 **Locked core** — `methodology.md`, `roles/`, and the locked reference skills (the
  `*-arsenal` tool skills, `htb-insane`, the scope rule). Stable behaviour + curated
  knowledge. Run **`bin/lock.sh`** to make it read-only so engagements can't touch it;
  **`bin/unlock.sh`** when you want to edit it on purpose.
- ✍️ **Learning library** — every skill tagged `stability: learning`. The **only** place new
  knowledge is written while working a target. The `learn` role appends here; the core stays frozen.

## Docs
- **[docs/SETUP.md](docs/SETUP.md)** — install & configure each tool (Claude Code, Codex, Gemini, local).
- **[docs/HOW-TO-CTF.md](docs/HOW-TO-CTF.md)** — the box workflow end to end.
- **[docs/LOCAL-MODELS.md](docs/LOCAL-MODELS.md)** — run fully offline on Ollama / LM Studio.

## What's in the library

Skills are organized by **domain** (`recon web api mobile cloud network ad ai-ml code-review
exploit-dev privesc defense payloads reporting automation tradecraft`) and tagged by **type**
and **mode**. Browse the generated **[`CATALOG.md`](CATALOG.md)**.

- **Arsenals** (`type: arsenal`) — tool selection per domain: *tool · why over alternatives ·
  exact command with flag gloss · gotcha* (`tools-recon`, `tools-web`, `tools-privesc`,
  `tools-ad-pivot`).
- **Techniques** (`type: technique`) — trigger-tagged exploit chains that auto-load on the
  right signal, across web/api/cloud/ai-ml and more.
- **Methodology / reporting / defense** — how to operate (dual-mode scope/RoE, hard-box
  discipline), how to report (bug-bounty/CVSS), and the blue-team half (detection engineering).

## Roadmap

- **Runtime engine (optional):** a provider-agnostic runner that drives the orchestration loop
  itself and calls Claude Code / Codex / Gemini / API / **local LLM** as interchangeable
  backends — real multi-agent + scope enforcement + audit logging for *every* tool.
- More domain skills across offensive + defensive (PRs welcome) — coverage matrix (OWASP/LLM/MITRE) next.

## Contributing

PRs welcome — especially new techniques from targets you've worked (CTF or bug bounty) and
defensive skills. The quickest contribution:
`cp framework/skills/_templates/technique.md framework/skills/<domain>/<slug>/SKILL.md`,
fill it in, then `ronin validate && ronin catalog && ronin build`, and open a PR. Full guide +
PR checklist in **[CONTRIBUTING.md](CONTRIBUTING.md)**. CI validates every skill against the
schema and checks build-drift, the scope rule, and CLI health on every push. Keep everything
authorized-use-framed.

## License

MIT — see [LICENSE](LICENSE). Use it on your own boxes and authorized engagements. Be ethical.
