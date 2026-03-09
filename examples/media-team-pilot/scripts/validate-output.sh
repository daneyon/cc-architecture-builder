#!/bin/bash
# validate-output.sh
# Quick validation of video output using ffprobe.
#
# Usage:
#   bash scripts/validate-output.sh output/video-name.mp4

set -euo pipefail

VIDEO="${1:-}"

if [[ -z "$VIDEO" ]]; then
  # Find most recent mp4 in output/
  VIDEO=$(ls -t output/*.mp4 2>/dev/null | head -1)
  if [[ -z "$VIDEO" ]]; then
    echo "No video file found in output/"
    exit 1
  fi
fi

if [[ ! -f "$VIDEO" ]]; then
  echo "File not found: $VIDEO"
  exit 1
fi

echo "=== Video Validation ==="
echo "File: $VIDEO"
echo ""

# Get format info
FORMAT_JSON=$(ffprobe -v quiet -print_format json -show_format -show_streams "$VIDEO")

# Extract key fields
DURATION=$(echo "$FORMAT_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['format'].get('duration', 'unknown'))")
SIZE=$(echo "$FORMAT_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['format'].get('size', 'unknown'))")
STREAMS=$(echo "$FORMAT_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('streams', [])))")

# Check video stream
HAS_VIDEO=$(echo "$FORMAT_JSON" | python3 -c "
import json, sys
d = json.load(sys.stdin)
streams = d.get('streams', [])
video = [s for s in streams if s.get('codec_type') == 'video']
if video:
    v = video[0]
    print(f\"YES - {v.get('codec_name', '?')} {v.get('width', '?')}x{v.get('height', '?')} @ {v.get('r_frame_rate', '?')} fps\")
else:
    print('NO')
")

# Check audio stream
HAS_AUDIO=$(echo "$FORMAT_JSON" | python3 -c "
import json, sys
d = json.load(sys.stdin)
streams = d.get('streams', [])
audio = [s for s in streams if s.get('codec_type') == 'audio']
if audio:
    a = audio[0]
    print(f\"YES - {a.get('codec_name', '?')} {a.get('sample_rate', '?')}Hz {a.get('channels', '?')}ch\")
else:
    print('NO')
")

# Format file size
SIZE_MB=$(python3 -c "print(f'{int(${SIZE:-0}) / 1024 / 1024:.1f}')")

echo "Duration:     ${DURATION}s"
echo "File size:    ${SIZE_MB} MB"
echo "Streams:      $STREAMS"
echo "Video stream: $HAS_VIDEO"
echo "Audio stream: $HAS_AUDIO"
echo ""

# Validation checks
ERRORS=0
WARNINGS=0

if [[ "$HAS_VIDEO" == "NO" ]]; then
  echo "[ERROR] No video stream found"
  ERRORS=$((ERRORS + 1))
fi

if [[ "$HAS_AUDIO" == "NO" ]]; then
  echo "[ERROR] No audio stream found"
  ERRORS=$((ERRORS + 1))
fi

if (( ERRORS > 0 )); then
  echo ""
  echo "RESULT: FAIL ($ERRORS errors, $WARNINGS warnings)"
  exit 1
else
  echo "RESULT: PASS ($WARNINGS warnings)"
  exit 0
fi
