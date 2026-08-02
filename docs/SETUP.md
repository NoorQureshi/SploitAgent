# Setup

Ronin is a tool-agnostic AI-assistant framework for **authorized lab practice only**
(HackTheBox, TryHackMe, Pro Labs, CPTS/OSCP). It keeps one tool-neutral knowledge
core in `framework/` and generates a native entry file per AI tool. Pick whichever
tool (and model) you have, point it at a confirmed target, and go.

> **Scope reminder:** Ronin only operates against targets you have confirmed are
> authorized — a lab VPN range or a declared exam range. Never point it at
> production, third-party, or public infrastructure.

> **TL;DR — use the `ronin` CLI.** The fastest path is `./setup.sh` then `ronin doctor`
> → `ronin install` → `ronin start claude`. The CLI wraps everything below (building
> entry files, installing tools, launching a backend). The sections here explain what it
> does under the hood and how to configure each tool by hand.

---

## 0. Prerequisites

- **OS:** Linux or macOS (Kali/Parrot are fine).
- **Base tooling:** `git`, `python3`, and the standard CTF toolkit (`nmap`, `ffuf`,
  etc.) already installed, or available from your distro's package manager.
- **Clone and build the entry files:**

```bash
git clone <repo> ronin && cd ronin
./adapters/build.sh all
```

`build.sh` reads the neutral core in `framework/` and writes one native entry file
per tool. Pass a specific tool instead of `all` to build just one:

```bash
./adapters/build.sh claude-code   # CLAUDE.md + .claude/
./adapters/build.sh codex         # AGENTS.md
./adapters/build.sh gemini        # GEMINI.md
```

Outputs at a glance:

| Tool         | Entry file(s)            |
| ------------ | ------------------------ |
| Claude Code  | `CLAUDE.md` + `.claude/` |
| Codex (etc.) | `AGENTS.md`              |
| Gemini CLI   | `GEMINI.md`              |

---

## 1. Claude Code — full multi-agent

The most capable path: reads `CLAUDE.md` plus `.claude/agents/` (subagents) and
`.claude/skills/` (loaded via the Skill tool). **This is the only tool with true
parallel sub-agents.** Uses Anthropic (Claude) models.

- **Install:** the official Claude Code CLI — npm package `@anthropic-ai/claude-code`,
  or the installer from Anthropic's docs. See the tool's official docs for the
  current install command.
- **Use:**

```bash
# from inside the repo — it auto-reads CLAUDE.md
claude
```

Then give it a confirmed, authorized target and let it drive the loop.

---

## 2. Codex CLI — single agent (and the local-model path)

Reads `AGENTS.md`. Runs a single agent. By default it uses OpenAI models with your
API key/login, but it is also the easiest route to a fully local model.

- **Install:** the OpenAI Codex CLI — npm `@openai/codex` or Homebrew. See OpenAI's
  Codex docs for the current install command.
- **Use:**

```bash
# from inside the repo — it reads AGENTS.md
codex
```

- **Local models:** Codex can run against a local Ollama model, or any
  OpenAI-compatible endpoint (e.g. LM Studio):

```bash
codex --oss            # pulls/uses a local Ollama model
```

  To point at any OpenAI-compatible endpoint, set the `base_url` + `model` in its
  model-provider config at `~/.codex/config.toml`. See **`docs/LOCAL-MODELS.md`** for
  the exact config.

---

## 3. Gemini CLI — single agent

Reads `GEMINI.md`. Runs a single agent using Google Gemini models (API key or Google
login). It is Google-model-focused; for local models prefer Codex or the Ronin
advisor (see LOCAL-MODELS.md).

- **Install:** the Google Gemini CLI — npm `@google/gemini-cli`. See Google's docs
  for the current install command.
- **Use:**

```bash
# from inside the repo — it reads GEMINI.md
gemini
```

---

## 4. Local models (Ollama / LM Studio) — quick pointer

Ronin works fully offline with a local model, two ways:

1. Point **Codex** at your local endpoint (see §2), or
2. Use the built-in advisor:

```bash
python3 adapters/local/ronin-advisor.py
```

Full details, model recommendations, and endpoint config live in
**`docs/LOCAL-MODELS.md`** — start there.

---

## 5. Rebuilding after you edit the framework

Edit anything under `framework/`, then re-run the build to refresh every tool's
entry file:

```bash
./adapters/build.sh all
```

**Locked-core rule:** only the learning library (`framework/skills/tech-*`) is meant
to change during engagements. Keep the stable core read-only, and unlock it only when
you deliberately intend to edit it:

```bash
bin/lock.sh      # make the stable core read-only
bin/unlock.sh    # unlock it to edit deliberately
```

See **`docs/HOW-TO-CTF.md`** for the full workflow.

---

## 6. Verify

After `./adapters/build.sh all`, confirm the entry files and directories exist:

```bash
ls CLAUDE.md AGENTS.md GEMINI.md
ls .claude/agents .claude/skills
```

Then open your tool of choice inside the repo and confirm it greets you
understanding the methodology (scope discipline, the recon → foothold → privesc
loop). If it does, you're set.

---

## Next steps

- **[HOW-TO-CTF.md](HOW-TO-CTF.md)** — the engagement workflow.
- **[LOCAL-MODELS.md](LOCAL-MODELS.md)** — running Ronin against a local model.
