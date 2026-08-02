#!/usr/bin/env bash
# Restore write access to the stable core (reverse of bin/lock.sh) so you can
# deliberately edit the methodology, roles, adapters, or a reference skill.
# After editing the framework, re-run ./adapters/build.sh all — and bin/lock.sh again.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

UNLOCK=(
  "$ROOT/framework/methodology.md"
  "$ROOT/framework/roles"
  "$ROOT/adapters"
  "$ROOT/bin"
  "$ROOT/ronin"
  "$ROOT/setup.sh"
)
for s in htb-insane tools-recon tools-web tools-privesc tools-ad-pivot; do
  UNLOCK+=("$ROOT/framework/skills/$s")
done

for p in "${UNLOCK[@]}"; do
  [ -e "$p" ] && chmod -R u+w "$p"
done
echo "🔓 unlocked the core (writable). Remember: edit framework/ → ./adapters/build.sh all → bin/lock.sh"
