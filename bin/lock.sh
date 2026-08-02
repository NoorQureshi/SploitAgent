#!/usr/bin/env bash
# Lock the STABLE CORE read-only so an engagement can't accidentally mutate it.
# The LEARNING library (framework/skills/tech-*, the template) stays writable — that's
# the only place new knowledge is meant to land while working boxes.
#
# Note: file permissions are local only (git tracks just the +x bit), so run this after
# cloning if you want hard enforcement. Reverse it with bin/unlock.sh.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

LOCKED=(
  "$ROOT/framework/methodology.md"
  "$ROOT/framework/roles"
  "$ROOT/adapters"
  "$ROOT/bin"
  "$ROOT/ronin"
  "$ROOT/setup.sh"
)
# reference skills are locked; tech-* (learning) are NOT
for s in htb-insane tools-recon tools-web tools-privesc tools-ad-pivot; do
  LOCKED+=("$ROOT/framework/skills/$s")
done

for p in "${LOCKED[@]}"; do
  [ -e "$p" ] && chmod -R a-w "$p"
done
echo "🔒 locked (read-only): methodology, roles, adapters, bin, reference skills (htb-insane, tools-*)"
echo "✍️  writable (learning): framework/skills/tech-*  +  framework/skills/TECHNIQUE-TEMPLATE.md"
echo "   (edit the core deliberately with bin/unlock.sh)"
