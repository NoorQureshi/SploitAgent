# SploitAgent — for Claude Code

You are in **SploitAgent**, an open library of security skills. Use it via the operating guide below,
which applies to every agent:

@AGENTS.md

## Claude Code specifics
- The files under `skills/` are in the standard **Agent Skills** format, organised by domain
  (`skills/<domain>/<slug>/SKILL.md`). To expose them to Claude Code — which discovers skills one
  directory deep — run `./install.sh` once; it links each skill into `~/.claude/skills/` (use
  `--project` for just this repo, `--uninstall` to remove). Opening Claude Code inside this repo also
  works without installing, via this file.
- When a task matches a skill's trigger, load that `skills/<domain>/<slug>/SKILL.md` and follow it.
- **Always load `tradecraft-scope-roe` first** and confirm authorization before acting.
