#!/usr/bin/env bash
# Generate per-tool entry files from the tool-neutral framework/ core.
# Source of truth: framework/methodology.md + framework/roles/ + framework/skills/
# Outputs: CLAUDE.md (+ .claude/ symlinks), AGENTS.md, GEMINI.md
# Usage: adapters/build.sh [claude-code|codex|gemini|all]   (default: all)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
FW="framework"
PROJECT="CTF Engagement Framework"
TARGET="${1:-all}"

# print a markdown file's body with any leading YAML frontmatter removed
strip_fm() { awk 'NR==1 && /^---[[:space:]]*$/ {infm=1; next} infm && /^---[[:space:]]*$/ {infm=0; next} !infm {print}' "$1"; }

ROLE_ORDER=(recon web ad privesc report learn)

gen_header() { # $1 = tool title
  printf '# %s — %s\n\n' "$1" "$PROJECT"
  printf '> Auto-generated from `%s/` by `adapters/build.sh`. **Edit the source, not this file.**\n' "$FW"
  printf '> For authorized CTF / lab practice only.\n\n'
}

build_claude() {
  { gen_header "CLAUDE.md · Claude Code"
    cat "$FW/methodology.md"
    printf '\n## Orchestration — Claude Code\n'
    printf 'You are the **orchestrator**. Each phase has a subagent in `.claude/agents/` '
    printf '(`htb-recon`, `htb-web`, `htb-ad`, `htb-privesc`, `htb-report`, `htb-learn`) — delegate to it and\n'
    printf 'route its findings to the next phase. Consult skills in `.claude/skills/` (the Skill tool) by phase.\n'
    printf 'Subagents run in isolation and cannot spawn other subagents. On independent targets (multiple\n'
    printf 'vhosts/hosts), run subagents in **parallel**.\n'
  } > CLAUDE.md
  # Claude Code discovers agents under .claude/agents (symlink to roles) and skills under
  # .claude/skills — flat discovery symlinks generated from the nested domain taxonomy.
  mkdir -p .claude
  ln -sfn "../$FW/roles"  .claude/agents
  python3 adapters/gen_index.py symlinks >/dev/null
  echo "  built CLAUDE.md + .claude/agents -> $FW/roles + .claude/skills discovery symlinks"
}

build_single() { # $1 = output file, $2 = tool title
  { gen_header "$2"
    cat "$FW/methodology.md"
    printf '\n## How to operate here (single agent)\n'
    printf 'This tool runs **one agent** (no sub-agents). Work the loop yourself, adopting each phase **role**\n'
    printf 'below in turn. When you enter a phase, open and read the relevant `%s/skills/<name>/SKILL.md`\n' "$FW"
    printf 'on demand (tool arsenals + known technique chains). Keep `notes.md` to the standard above; work one\n'
    printf 'lead at a time unless told to go full-auto.\n'
    printf '\n## Phase roles (adopt in sequence)\n'
    for r in "${ROLE_ORDER[@]}"; do
      f="$FW/roles/htb-$r.md"; [ -f "$f" ] || continue
      printf '\n### Role: %s\n' "$r"
      strip_fm "$f"
    done
    printf '\n## Skills index (by domain)\n'
    printf 'Open the matching `%s/skills/<domain>/<slug>/SKILL.md` when its trigger fits the phase. Full table: `CATALOG.md`.\n\n' "$FW"
    python3 adapters/gen_index.py index
  } > "$1"
  echo "  built $1"
}

case "$TARGET" in
  claude-code) build_claude ;;
  codex)       build_single AGENTS.md "AGENTS.md · Codex & AGENTS.md-compatible tools" ;;
  gemini)      build_single GEMINI.md "GEMINI.md · Gemini CLI" ;;
  all)
    build_claude
    build_single AGENTS.md "AGENTS.md · Codex & AGENTS.md-compatible tools"
    build_single GEMINI.md "GEMINI.md · Gemini CLI"
    ;;
  *) echo "usage: adapters/build.sh [claude-code|codex|gemini|all]" >&2; exit 2 ;;
esac
# Always regenerate the browsable catalog + machine index from the taxonomy.
python3 adapters/gen_index.py catalog >/dev/null
echo "done ($TARGET)."
