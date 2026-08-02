# Local models — Ollama & LM Studio

Run Ronin **fully offline** with a local model. Both Ollama and LM Studio expose an
**OpenAI-compatible** API, so anything that speaks that protocol can use Ronin's brain.

> Authorized lab practice only. A local model keeps your engagement data on your machine —
> nothing leaves the box.

## Two ways to use a local model

| Path | What it does | Runs commands itself? |
|---|---|---|
| **A. Codex → local endpoint** | Point the Codex CLI at Ollama/LM Studio; it reads `AGENTS.md` and executes tools like normal | ✅ yes |
| **B. Ronin advisor** | `adapters/local/ronin-advisor.py` — a tiny offline chat that loads the framework and coaches you | ❌ no — you run the commands |

Path A is the full experience (the agent runs `nmap`, `ffuf`, etc.). Path B needs zero extra
tooling and is great as a private, offline "coach" when you want to drive the keyboard yourself.

---

## 1. Install a runner

### Ollama
```bash
# install from https://ollama.com, then pull a capable coder model:
ollama pull qwen2.5-coder:14b        # good all-round; try :7b on light hardware
ollama pull llama3.1:8b              # alternative
ollama serve                         # serves the API on http://localhost:11434
```
- OpenAI-compatible base URL: **`http://localhost:11434/v1`** · API key: any string (e.g. `ollama`).

### LM Studio
1. Install LM Studio (GUI) from https://lmstudio.ai and **download a model** (e.g. a
   Qwen2.5-Coder or Llama-3.1 GGUF).
2. Open the **Developer / Local Server** tab and **Start Server**.
- OpenAI-compatible base URL: **`http://localhost:1234/v1`** · API key: any string (e.g. `lm-studio`).
- The model name is whatever LM Studio shows for the loaded model.

**Model tips:** prefer *coder/instruct* models; 14B+ reason noticeably better for exploitation
than 7B. Give the model as much context length as your RAM/VRAM allows — engagement notes get
long. Everything runs locally, so pick the largest model you can serve comfortably.

---

## 2. Path A — Codex against a local model (full tool execution)

Codex reads `AGENTS.md` (build it first: `./adapters/build.sh codex`).

**Ollama** — Codex has first-class local support:
```bash
codex --oss -m qwen2.5-coder:14b        # uses your local Ollama automatically
```

**LM Studio (or any OpenAI-compatible endpoint)** — add a provider in `~/.codex/config.toml`:
```toml
[model_providers.lmstudio]
name = "LM Studio (local)"
base_url = "http://localhost:1234/v1"
env_key = "LOCAL_API_KEY"        # value can be any non-empty string

[profiles.local]
model = "your-loaded-model-name"
model_provider = "lmstudio"
```
```bash
export LOCAL_API_KEY=lm-studio
codex --profile local
```
Then work the box normally — Codex follows `AGENTS.md` and runs the commands.
(Check `codex --help` / the Codex docs for the exact flag names in your version.)

---

## 3. Path B — the built-in Ronin advisor (offline, no extra tools)

A stdlib-only Python client that loads the framework as the system prompt and coaches you
through the box. It does **not** run commands — it hands you the exact next command and waits
for you to paste the output.

```bash
# Ollama
python3 adapters/local/ronin-advisor.py --provider ollama   --model qwen2.5-coder:14b

# LM Studio
python3 adapters/local/ronin-advisor.py --provider lmstudio --model your-loaded-model-name

# any OpenAI-compatible endpoint
python3 adapters/local/ronin-advisor.py --base-url http://host:port/v1 --api-key KEY --model M
```

In-session commands:
```
/skill <name>   inject a skill file (e.g. /skill tools-recon) for the current phase
/skills         list available skills
/reset          clear the conversation (keeps the framework system prompt)
/save <file>    write the transcript to a file (paste into your notes.md)
/quit           exit
```
It enforces the scope rule (won't proceed until you confirm the target is an authorized lab)
and keeps to the five-beat teaching-notes style.

---

## 4. Which should I use?

- Want the agent to actually run tools offline → **Path A (Codex + local)**.
- Want a private offline second brain while you drive → **Path B (advisor)**.
- Have an API subscription and don't need offline → just use Claude Code / Codex / Gemini
  normally (see [SETUP.md](SETUP.md)).

For the box workflow itself, see [HOW-TO-CTF.md](HOW-TO-CTF.md).

> Roadmap: the optional Ronin runtime engine will drive full **multi-agent** orchestration
> against any local model (not just single-agent), with scope enforcement and audit logging.
