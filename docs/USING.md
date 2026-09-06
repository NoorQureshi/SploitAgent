# Using Ronin

Ronin is a **library of security skills** in the standard Agent-Skills format
(`skills/<domain>/<slug>/SKILL.md` with a `description:` trigger line). You load the skills
into whatever AI agent you use; the agent auto-selects the right skill from the task.

## Claude Code
Claude Code discovers skills under a `.claude/skills/` directory. Point it at Ronin's skills:

```bash
git clone https://github.com/noorqureshi/ronin
ln -s "$PWD/ronin/skills" ~/.claude/skills/ronin     # or copy: cp -r ronin/skills/* ~/.claude/skills/
```

Then describe your authorized target ("bug-bounty program acme.com, in scope, run recon") and
the relevant skills load automatically.

## Codex / Gemini / other agents
Any agent that reads skill/instruction files can use Ronin: point it at the `skills/` directory,
or paste a specific `SKILL.md` into context when you start a task. The skills are plain Markdown —
no runtime required.

## Local models (Ollama / LM Studio)
Same idea — the skills are just text. Load the domain(s) you need into the model's context, or
use an agent framework that reads the `skills/` folder.

## Browsing & maintenance
- **[`CATALOG.md`](../CATALOG.md)** — the full, browsable list of every skill.
- Validate and regenerate the catalog after editing skills:
  ```bash
  python3 tools/catalog.py validate   # schema-check every skill
  python3 tools/catalog.py            # validate + regenerate CATALOG.md
  ```

## The rule that comes first
Every engagement starts with **scope**. Load `tradecraft-scope-roe` and confirm you're inside a
signed pentest scope, a bug-bounty program you're in scope for, or systems you own/are authorized
to test. Never point these skills at anything else.
