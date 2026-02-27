#!/bin/bash
# assemble-video.sh
# Combines scene images + audio into a final .mp4 video using ffmpeg.
# Applies Ken Burns effect (zoom/pan) on images and crossfade transitions.
#
# Usage:
#   bash scripts/assemble-video.sh \
#     --script temp/script.json \
#     --images temp/assets/images/ \
#     --audio temp/assets/audio/ \
#     --output output/

set -euo pipefail

# --- Parse arguments ---
SCRIPT_FILE=""
IMAGES_DIR=""
AUDIO_DIR=""
OUTPUT_DIR=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --script) SCRIPT_FILE="$2"; shift 2 ;;
    --images) IMAGES_DIR="$2"; shift 2 ;;
    --audio)  AUDIO_DIR="$2"; shift 2 ;;
    --output) OUTPUT_DIR="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$SCRIPT_FILE" || -z "$IMAGES_DIR" || -z "$AUDIO_DIR" || -z "$OUTPUT_DIR" ]]; then
  echo "Usage: assemble-video.sh --script FILE --images DIR --audio DIR --output DIR"
  exit 1
fi

# --- Check dependencies ---
if ! command -v ffmpeg &> /dev/null; then
  echo "ERROR: ffmpeg is not installed. Install it with: apt install ffmpeg (or brew install ffmpeg)"
  exit 1
fi

if ! command -v python3 &> /dev/null; then
  echo "ERROR: python3 is not found in PATH"
  exit 1
fi

# --- Read script metadata ---
TITLE=$(python3 -c "import json; d=json.load(open('$SCRIPT_FILE')); print(d.get('title', 'untitled'))")
SCENE_COUNT=$(python3 -c "import json; d=json.load(open('$SCRIPT_FILE')); print(len(d.get('scenes', [])))")
TRANSITION_DURATION=1

echo "=== Video Assembly ==="
echo "Title: $TITLE"
echo "Scenes: $SCENE_COUNT"
echo ""

# --- Slugify title for filename ---
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//')
OUTPUT_FILE="$OUTPUT_DIR/${SLUG}.mp4"

mkdir -p "$OUTPUT_DIR"

# --- Create temp directory for scene clips ---
WORK_DIR=$(mktemp -d)
trap "rm -rf $WORK_DIR" EXIT

echo "Working directory: $WORK_DIR"

# --- Generate scene video clips ---
CONCAT_LIST="$WORK_DIR/concat.txt"
> "$CONCAT_LIST"

for i in $(seq 1 "$SCENE_COUNT"); do
  PADDED=$(printf "%03d" "$i")
  IMAGE="$IMAGES_DIR/scene_${PADDED}.png"
  AUDIO="$AUDIO_DIR/scene_${PADDED}.mp3"

  if [[ ! -f "$IMAGE" ]]; then
    echo "WARNING: Missing image for scene $i: $IMAGE"
    continue
  fi

  # Get scene duration from script
  DURATION=$(python3 -c "
import json
d=json.load(open('$SCRIPT_FILE'))
scenes = d.get('scenes', [])
scene = next((s for s in scenes if s['scene_number'] == $i), None)
print(scene.get('duration_seconds', 8) if scene else 8)
")

  SCENE_CLIP="$WORK_DIR/scene_${PADDED}.mp4"
  FRAMES=$((DURATION * 30))

  echo "Processing scene $i ($DURATION seconds)..."

  # Ken Burns: subtle zoom from 1.0 to 1.15 over the scene duration
  ZOOM_INCREMENT=$(python3 -c "print(f'{0.15 / $FRAMES:.8f}')")

  if [[ -f "$AUDIO" ]]; then
    # Scene with audio narration
    ffmpeg -y -loglevel warning \
      -loop 1 -i "$IMAGE" \
      -i "$AUDIO" \
      -t "$DURATION" \
      -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,zoompan=z='min(zoom+${ZOOM_INCREMENT},1.15)':d=${FRAMES}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30" \
      -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
      -c:a aac -b:a 192k -ar 44100 \
      -shortest \
      "$SCENE_CLIP"
  else
    # Scene without audio (silent)
    ffmpeg -y -loglevel warning \
      -loop 1 -i "$IMAGE" \
      -f lavfi -i "anullsrc=r=44100:cl=stereo" \
      -t "$DURATION" \
      -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,zoompan=z='min(zoom+${ZOOM_INCREMENT},1.15)':d=${FRAMES}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30" \
      -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
      -c:a aac -b:a 192k -ar 44100 \
      -shortest \
      "$SCENE_CLIP"
  fi

  echo "file '$SCENE_CLIP'" >> "$CONCAT_LIST"
  echo "  -> Scene $i clip created"
done

# --- Concatenate all scene clips ---
echo ""
echo "Concatenating scenes..."

CONCAT_OUTPUT="$WORK_DIR/concatenated.mp4"
ffmpeg -y -loglevel warning \
  -f concat -safe 0 -i "$CONCAT_LIST" \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  "$CONCAT_OUTPUT"

# --- Apply fade-in at start and fade-out at end ---
echo "Applying fade effects..."

TOTAL_DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$CONCAT_OUTPUT" | cut -d. -f1)
FADE_OUT_START=$((TOTAL_DURATION - 2))

ffmpeg -y -loglevel warning \
  -i "$CONCAT_OUTPUT" \
  -vf "fade=t=in:st=0:d=1.5,fade=t=out:st=${FADE_OUT_START}:d=2" \
  -af "afade=t=in:st=0:d=1.5,afade=t=out:st=${FADE_OUT_START}:d=2" \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  "$OUTPUT_FILE"

echo ""
echo "=== Assembly Complete ==="
echo "Output: $OUTPUT_FILE"
echo "Duration: ~${TOTAL_DURATION}s"

# File size
SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
echo "Size: $SIZE"
echo ""
echo "Run '/review-video' to validate the output."
