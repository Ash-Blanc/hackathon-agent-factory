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
