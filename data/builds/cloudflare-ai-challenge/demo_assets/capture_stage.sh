#!/usr/bin/env bash
URL="${1:-http://localhost:3000}"
echo "Launching 1600x900 borderless capture window for $URL..."
if command -v chromium &> /dev/null; then
  chromium --app="$URL" --window-size=1600,900 --window-position=50,50 --force-device-scale-factor=1 &
elif command -v google-chrome &> /dev/null; then
  google-chrome --app="$URL" --window-size=1600,900 --window-position=50,50 --force-device-scale-factor=1 &
else
  echo "Open browser window at 1600x900 resolution."
fi
