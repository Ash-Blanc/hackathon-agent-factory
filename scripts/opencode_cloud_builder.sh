#!/usr/bin/env bash
set -e

WORKSPACE_DIR="$1"
if [ -z "$WORKSPACE_DIR" ]; then
  echo "Usage: ./opencode_cloud_builder.sh <workspace_dir>"
  exit 1
fi

echo "🚀 Starting OpenCode cloud sandbox builder in $WORKSPACE_DIR..."
cd "$WORKSPACE_DIR"

if [ -f "TASK.md" ]; then
  echo "📋 Task identified:"
  head -n 10 TASK.md
  echo "----------------------------------------"
  /home/ash/.opencode/bin/opencode run "Read TASK.md and initialize the complete project repository with frontend, backend, test suite, and README.md with architecture diagram."
else
  echo "❌ Error: TASK.md not found in $WORKSPACE_DIR"
  exit 1
fi
