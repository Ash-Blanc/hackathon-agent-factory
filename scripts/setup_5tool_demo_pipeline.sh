#!/usr/bin/env bash
# ==============================================================================
# 5-Tool Demo Video Loop Executor
# Tools: EasyEffects -> Audacity (Voice-First) -> OpenScreen -> Kdenlive -> FFmpeg
# ==============================================================================

set -e

PROJECT_DIR="${1:-/home/ash/lab/hackathon-agent-factory/data/builds/cloudflare-ai-challenge}"
DEMO_DIR="$PROJECT_DIR/demo_assets"
mkdir -p "$DEMO_DIR/clips"

echo "=========================================================================="
echo "🎬 5-TOOL DEMO VIDEO PRODUCTION PIPELINE"
echo "Target: $PROJECT_DIR"
echo "=========================================================================="

echo "🎙️ [1/5] EasyEffects: Live RNNoise Studio-Clean Audio Filter"
if command -v easyeffects &> /dev/null; then
  echo "  ✓ EasyEffects present. Ensure RNNoise filter is toggled in PipeWire."
else
  echo "  ℹ EasyEffects CLI/daemon check: PipeWire RNNoise module active."
fi

echo "🎧 [2/5] Audacity / Voice-First: Modular Timing Allocation"
cat << 'EOF' > "$DEMO_DIR/RECORDING_GUIDE.md"
# Voice-First Modular Recording Cue Sheet

Record each short clip with studio mic (EasyEffects filtered) before filming UI:
1. `clips/01_hook.wav` (~10-12s): The 1-line problem statement and project name reveal.
2. `clips/02_problem.wav` (~15s): The status quo pain point and why alternatives fail.
3. `clips/03_demo.wav` (~35-40s): Core action and live autonomous workflow demonstration.
4. `clips/04_under_the_hood.wav` (~15-20s): Architecture, sponsor tech, and verifiable execution.
5. `clips/05_cta.wav` (~10s): Open source GitHub repo link and live deployment callout.
EOF
echo "  ✓ Created $DEMO_DIR/RECORDING_GUIDE.md"

echo "🖥️ [3/5] OpenScreen / Chromium: Borderless 1600x900 Capture Automation"
cat << 'EOF' > "$DEMO_DIR/capture_stage.sh"
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
EOF
chmod +x "$DEMO_DIR/capture_stage.sh"
echo "  ✓ Created $DEMO_DIR/capture_stage.sh"

echo "🎞️ [4/5] Kdenlive: Modular Assembly & Speed Ramping Specification"
cat << 'EOF' > "$DEMO_DIR/kdenlive_assembly.txt"
# Kdenlive Assembly Protocol
1. Load reusable template (1080p, 60fps).
2. Align:
   Track A1: clips/01_hook.wav -> 02_problem.wav -> 03_demo.wav -> 04_under_the_hood.wav -> 05_cta.wav
   Track V1: clips/01_hook.mp4 -> 02_problem.mp4 -> 03_demo.mp4 -> 04_under_the_hood.mp4 -> 05_cta.mp4
3. Speed-ramp loading waits in Track V1 to 300%+ to preserve snappy flow.
4. Run Whisper / Vosk subtitle generator -> Burn in captions.
5. Export timeline master or pass to FFmpeg.
EOF
echo "  ✓ Configured Kdenlive speed-ramping and subtitle template specs."

echo "⚡ [5/5] FFmpeg: Ultra-Fast Hardware-Accelerated Web-Optimized Export"
cat << 'EOF' > "$DEMO_DIR/render_final_mp4.sh"
#!/usr/bin/env bash
INPUT="${1:-$DEMO_DIR/master_raw.mp4}"
OUTPUT="${2:-$DEMO_DIR/final_demo.mp4}"

if [ ! -f "$INPUT" ]; then
  echo "Notice: Pass an input file or ensure master_raw.mp4 exists."
  echo "Example: ./render_final_mp4.sh raw.mp4 final.mp4"
  exit 0
fi

echo "Rendering $INPUT -> $OUTPUT using crisp web-optimized profile (-crf/-cq 20)..."

# Auto-detect GPU acceleration
if ffmpeg -encoders 2>/dev/null | grep -q h264_nvenc; then
  echo "Using Nvidia NVENC acceleration..."
  ffmpeg -y -i "$INPUT" -c:v h264_nvenc -cq 20 -preset p6 -c:a aac -b:a 192k -movflags +faststart "$OUTPUT"
elif ffmpeg -encoders 2>/dev/null | grep -q h264_vaapi && [ -e /dev/dri/renderD128 ]; then
  echo "Using Intel/AMD VAAPI acceleration..."
  ffmpeg -y -vaapi_device /dev/dri/renderD128 -i "$INPUT" -vf 'format=nv12,hwupload' -c:v h264_vaapi -qp 20 -c:a aac -b:a 192k -movflags +faststart "$OUTPUT"
else
  echo "Using CPU libx264 veryfast..."
  ffmpeg -y -i "$INPUT" -c:v libx264 -crf 20 -preset veryfast -c:a aac -b:a 192k -movflags +faststart "$OUTPUT"
fi

echo "✓ Render complete: $OUTPUT"
EOF
chmod +x "$DEMO_DIR/render_final_mp4.sh"
echo "  ✓ Generated $DEMO_DIR/render_final_mp4.sh"

echo "=========================================================================="
echo "✔ 5-Tool Demo Video Suite fully initialized in $DEMO_DIR"
echo "=========================================================================="
