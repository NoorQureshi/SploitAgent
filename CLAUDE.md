# SploitAgent — for Claude Code

You are in **SploitAgent**, an open library of security skills. Use it via the operating guide below,
which applies to every agent:

@AGENTS.md

## Claude Code specifics
- The files under `skills/` are in the standard **Agent Skills** format. To make them available in
  every project, symlink them into your user scope once:
  `ln -s "$PWD/skills" ~/.claude/skills/sploitagent`
- When a task matches a skill's trigger, load that `skills/<domain>/<slug>/SKILL.md` and follow it.
- **Always load `tradecraft-scope-roe` first** and confirm authorization before acting.
