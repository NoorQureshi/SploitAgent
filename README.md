<h1 align="center">🥷 Ronin</h1>

<p align="center">
  <b>A masterless AI operator for authorized CTF / HTB labs — bring your own blade.</b><br>
  One engagement brain. Plug it into <b>Claude Code</b>, <b>Codex</b>, <b>Gemini CLI</b>, or a <b>local model</b>.
</p>

<p align="center">
  <a href="https://github.com/NoorQureshi/ronin/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/NoorQureshi/ronin/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="scope" src="https://img.shields.io/badge/scope-authorized_labs_only-red">
  <img alt="tools" src="https://img.shields.io/badge/works_with-Claude_Code_·_Codex_·_Gemini_·_local-6E56CF">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-blue">
</p>

---

A ronin serves no single master and fights with whatever weapon is at hand. This framework
is the same: the *knowledge* of how to work a box — a full engagement methodology, phase
playbooks, and a growing library of tool arsenals and learned exploit techniques — kept in
**one tool-neutral core** and compiled into a native entry file for **whatever AI CLI you
already run**.

> ⚠️ **Authorized lab practice only.** Scope discipline is the first instruction in every
> component: Ronin refuses to act until a target is confirmed inside an authorized lab range
> (HackTheBox / TryHackMe / Pro Labs / CPTS-OSCP). Don't point it at anything you don't own
> or aren't explicitly authorized to test.

## How it works

The valuable part — *how to think through a box* — is portable knowledge. Ronin keeps it in
**one source** and generates each tool's entry file from it, so nothing is written twice and
nothing drifts.

```
ronin                         ← the CLI: doctor · install · build · start · local · new · lock
setup.sh                      ← one-time bootstrap (build + put `ronin` on PATH)
framework/                    ← SINGLE SOURCE OF TRUTH
  methodology.md                the loop · scope rule · note-taking standard          🔒 locked
  roles/                        phase playbooks: recon·web·ad·privesc·report·learn     🔒 locked
  skills/
    tools-* · htb-insane        tool arsenals + hard-box discipline                    🔒 locked
    tech-*                      learned exploit chains — the part that GROWS           ✍️  learning
adapters/
  build.sh                      generator → writes the per-tool entry files below
  local/ronin-advisor.py        offline advisor for Ollama / LM Studio
bin/lock.sh · bin/unlock.sh     freeze / deliberately edit the locked core
docs/                           SETUP · HOW-TO-CTF · LOCAL-MODELS
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

## The `ronin` command

A normal CLI front door — `ronin --help` and `ronin <cmd> --help` everywhere:

| Command | What it does |
|---|---|
| `ronin doctor` | Detect your OS + list which AI backends and pentest tools are installed |
| `ronin install [--group recon\|web\|ad] [--yes]` | Install the missing tools via your OS package manager (apt/brew/pacman/dnf), with pipx/go fallbacks |
| `ronin start claude\|codex\|gemini` | Launch that AI backend inside the repo |
| `ronin local --provider ollama\|lmstudio --model <m>` | Start the offline advisor against a local model |
| `ronin new <box> --target <ip>` | Scaffold an engagement dir (`scope.txt`, `notes.md`, `state.md`, `recon/` …) |
| `ronin build [all\|claude-code\|codex\|gemini]` | Regenerate the entry files after editing `framework/` |
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

When a box teaches a reusable trick, the **learn** role captures it as a new
`framework/skills/tech-<slug>/SKILL.md` (from `TECHNIQUE-TEMPLATE.md`) and indexes it — so the
next box with the same signal auto-applies it. Techniques already forged from real boxes:

- **`tech-mongo-agg-facet-bypass`** — MongoDB aggregation stage-allowlist bypass via
  `$facet` → `$unionWith` to read sibling collections.
- **`tech-webauthn-software-authenticator`** — register/log in to a WebAuthn RP with a
  self-built software authenticator when attestation is `none`.
- **`tech-gopher-redis-rce`** — SSRF → internal Redis → RCE via `gopher://`.

Edit anything under `framework/`, then re-run `./adapters/build.sh all` to refresh every tool.

## Locked core vs learning library

The framework improves without ever corrupting what makes it reliable — it's split in two:

- 🔒 **Locked core** — `methodology.md`, `roles/`, and the reference skills (`tools-*`,
  `htb-insane`). Stable behaviour + curated knowledge. Run **`bin/lock.sh`** to make it
  read-only so engagements can't touch it; **`bin/unlock.sh`** when you want to edit it on purpose.
- ✍️ **Learning library** — `framework/skills/tech-*`. The **only** place new knowledge is
  written while working a box. The `learn` role appends here; the core stays frozen.

## Docs
- **[docs/SETUP.md](docs/SETUP.md)** — install & configure each tool (Claude Code, Codex, Gemini, local).
- **[docs/HOW-TO-CTF.md](docs/HOW-TO-CTF.md)** — the box workflow end to end.
- **[docs/LOCAL-MODELS.md](docs/LOCAL-MODELS.md)** — run fully offline on Ollama / LM Studio.

## What's in the arsenal

- **Reference skills (by phase):** `htb-insane` (hard-box discipline), `tools-recon`,
  `tools-web`, `tools-privesc`, `tools-ad-pivot` — each entry: *tool · why over alternatives ·
  exact command with flag gloss · gotcha*.
- **Technique skills:** trigger-tagged `tech-*` exploit chains that auto-load on the right signal.

## Roadmap

- **Runtime engine (optional):** a provider-agnostic runner that drives the orchestration loop
  itself and calls Claude Code / Codex / Gemini / API / **local LLM** as interchangeable
  backends — real multi-agent + scope enforcement + audit logging for *every* tool.
- More `tools-*` arsenals and community `tech-*` techniques (PRs welcome).

## Contributing

PRs welcome — especially new `tech-*` techniques from boxes you've rooted. The quickest
contribution: `cp framework/skills/TECHNIQUE-TEMPLATE.md framework/skills/tech-<slug>/SKILL.md`,
fill it in, index it, `ronin build all`, open a PR. Full guide + PR checklist in
**[CONTRIBUTING.md](CONTRIBUTING.md)**. CI checks build-drift, the scope rule, and CLI health
on every push. Keep everything authorized-lab-framed.

## License

MIT — see [LICENSE](LICENSE). Use it on your own boxes and authorized engagements. Be ethical.
