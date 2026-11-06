#!/usr/bin/env bash
# One-time setup: installs uv if missing, creates .env, syncs dependencies.
# Run from this folder:  bash setup.sh
set -euo pipefail
cd "$(dirname "$0")"

export PATH="$HOME/.local/bin:$PATH"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv not found, installing..."
  case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*)
      powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" ;;
    *)
      curl -LsSf https://astral.sh/uv/install.sh | sh ;;
  esac
  export PATH="$HOME/.local/bin:$PATH"
fi
uv --version

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example. Edit it and fill in your provider settings."
else
  echo ".env already exists, leaving it untouched."
fi

uv sync
echo
echo "Done. If 'uv' is still not found in a new terminal, restart it so PATH updates."
echo "Try: uv run labs/wf00_augmented_llm.py"
