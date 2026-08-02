#!/usr/bin/env bash
# One-time bootstrap: build the per-tool entry files and put `ronin` on your PATH.
# After this:  ronin doctor  →  ronin install  →  ronin start claude
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"; cd "$ROOT"

chmod +x ronin setup.sh adapters/build.sh adapters/local/ronin-advisor.py bin/lock.sh bin/unlock.sh 2>/dev/null || true
./adapters/build.sh all

BIN="$HOME/.local/bin"; mkdir -p "$BIN"
ln -sfn "$ROOT/ronin" "$BIN/ronin"

echo
echo "✅ ronin installed → $BIN/ronin"
case ":$PATH:" in
  *":$BIN:"*) : ;;
  *) echo "⚠️  add ~/.local/bin to your PATH, e.g.:"
     echo "      echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc && source ~/.zshrc" ;;
esac
echo
echo "next:"
echo "   ronin doctor              # what's installed on this box"
echo "   ronin install            # install missing pentest tools for your OS"
echo "   ronin start claude       # or: codex | gemini   ·   ronin local --model <m> for offline"
