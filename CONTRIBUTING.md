# Contributing to Ronin

Thanks for helping sharpen the framework. Ronin is for **authorized** security practice
only (HackTheBox / TryHackMe / Pro Labs / CPTS-OSCP) — every contribution must keep that
framing. No real targets, no live credentials/flags, no content aimed at systems you don't
own or aren't authorized to test.

## The golden rule: edit the source, then rebuild

`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, and `.claude/` are **generated**. Never edit them by
hand — edit the source under `framework/` and regenerate:

```bash
./adapters/build.sh all      # or:  ronin build all
```

CI fails if the generated files are out of date, so always rebuild before committing.

## Locked core vs learning library

- 🔒 **Locked core** — `framework/methodology.md`, `framework/roles/`, and the reference
  skills (`tools-*`, `htb-insane`). Changing these changes the agent's behaviour; do it
  deliberately (`bin/unlock.sh` → edit → `./adapters/build.sh all` → `bin/lock.sh`) and
  explain *why* in your PR.
- ✍️ **Learning library** — `framework/skills/tech-*`. New exploit techniques land here.
  This is the easiest and most welcome contribution.

## Add a technique skill (most common PR)

```bash
cp framework/skills/TECHNIQUE-TEMPLATE.md framework/skills/tech-<slug>/SKILL.md
```
Fill it in:
- **`description:`** frontmatter with concrete **trigger signals** (service/version, vuln
  class, tool-output patterns, error strings) — auto-loading is only as good as this line.
- **when it applies · why it works · method (exact commands) · gotchas · verify success.**
- Generalize: no box-specific IPs/creds/flags (reference the box only under "Learned on").

Then index it in `framework/skills/README.md` under the learning section, and rebuild.

## Add a tool to `ronin install`

Edit the `TOOLS` catalog in `./ronin` (a locked-core file — unlock first). Give the check
binary, the package name per manager where you know it (`apt`/`brew`/`pacman`/`dnf`), and a
`pipx`/`go` fallback if it isn't packaged. Keep entries accurate — test on your OS.

## Before you open a PR

Run the same checks CI runs:
```bash
python3 -m py_compile ronin adapters/local/ronin-advisor.py
bash -n adapters/build.sh bin/lock.sh bin/unlock.sh setup.sh
./adapters/build.sh all && git diff --quiet -- CLAUDE.md AGENTS.md GEMINI.md && echo "no drift ✓"
./ronin doctor >/dev/null && echo "cli ok ✓"
```

Checklist:
- [ ] Source edited under `framework/` (or `ronin`), generated files rebuilt.
- [ ] Authorized-lab framing; no real targets/creds/flags.
- [ ] New technique has strong trigger keywords and is indexed.
- [ ] CI is green.

## Style
Match the house voice: terse, teach-the-mechanism, *tool · why over alternatives · exact
command with a flag gloss · gotcha*. Small focused skills beat one giant file.
