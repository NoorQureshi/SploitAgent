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
- ✍️ **Learning library** — every skill tagged `stability: learning`. New techniques land here.
  This is the easiest and most welcome contribution.

## Add a skill (most common PR)

Skills live under a domain: `framework/skills/<domain>/<slug>/SKILL.md`. Domains:
`recon web api mobile cloud network ad ai-ml code-review exploit-dev privesc defense
payloads reporting automation tradecraft`.

```bash
cp framework/skills/_templates/technique.md framework/skills/<domain>/<slug>/SKILL.md
# (arsenal.md / methodology.md templates also available)
ronin validate      # schema-check your frontmatter
ronin catalog       # regenerate CATALOG.md + index + discovery symlinks
```

Fill it in:
- **Frontmatter** — required: `name` (domain-prefixed kebab-case, e.g. `web-ssrf`),
  `description`, `domain`, `type`, `stability` (`learning` for new techniques), `modes`
  (`ctf`/`bugbounty`/`defense`), `schema_version: 1`. Optional but encouraged:
  `severity`, `owasp`/`owasp_llm`/`owasp_api`, `mitre`, `cwe`, `tools`.
- **`description:`** must pack concrete **trigger signals** (service/version, vuln class,
  tool-output patterns, error strings, ports) — auto-loading is only as good as this line.
- **Body:** when it applies · why it works · method (exact commands + flag gloss) · gotchas
  · verify success · references.
- Generalize: no real IPs/creds/flags (reference a box only under a "Learned on" note).

The catalog and index are **generated** — you don't hand-edit `CATALOG.md` or the README
index; `ronin catalog` regenerates them from your frontmatter.

## Add a tool to `ronin install`

Edit the `TOOLS` catalog in `./ronin` (a locked-core file — unlock first). Give the check
binary, the package name per manager where you know it (`apt`/`brew`/`pacman`/`dnf`), and a
`pipx`/`go` fallback if it isn't packaged. Keep entries accurate — test on your OS.

## Before you open a PR

Run the same checks CI runs:
```bash
python3 -m py_compile ronin adapters/gen_index.py adapters/local/ronin-advisor.py
bash -n adapters/build.sh bin/lock.sh bin/unlock.sh setup.sh
./ronin validate                                                   # skills pass the schema
./adapters/build.sh all && git diff --quiet -- CLAUDE.md AGENTS.md GEMINI.md CATALOG.md && echo "no drift ✓"
./ronin doctor >/dev/null && echo "cli ok ✓"
```

Checklist:
- [ ] Skill under the right `framework/skills/<domain>/`, frontmatter passes `ronin validate`.
- [ ] Authorized-use framing; correct `modes:`; no real targets/creds/flags.
- [ ] Strong trigger signals in `description:`; mappings (`owasp`/`mitre`/`cwe`) where they apply.
- [ ] Generated files rebuilt (`ronin build`) and committed; CI is green.

## Style
Match the house voice: terse, teach-the-mechanism, *tool · why over alternatives · exact
command with a flag gloss · gotcha*. Small focused skills beat one giant file.
