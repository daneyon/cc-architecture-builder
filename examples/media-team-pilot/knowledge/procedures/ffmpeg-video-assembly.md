# ffmpeg Video Assembly Procedure

## Prerequisites
- ffmpeg installed (`ffmpeg -version` to verify)
- Scene images in `temp/assets/images/scene_NNN.png`
- Scene audio in `temp/assets/audio/scene_NNN.mp3`
- Script timing in `temp/script.json`

## Step-by-Step Assembly

### 1. Create Individual Scene Clips

For each scene, combine its image (with Ken Burns effect) and audio:

```bash
# Variables per scene
DURATION=8          # From script.json
FRAMES=$((DURATION * 30))
ZOOM_INC=$(python3 -c "print(f'{0.15 / $FRAMES:.8f}')")

ffmpeg -y \
  -loop 1 -i scene_001.png \
  -i scene_001.mp3 \
  -t $DURATION \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,zoompan=z='min(zoom+${ZOOM_INC},1.15)':d=${FRAMES}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30" \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 44100 \
  -shortest \
  scene_001.mp4
```

### 2. Create Concat List

```bash
# concat.txt
file 'scene_001.mp4'
file 'scene_002.mp4'
file 'scene_003.mp4'
```

### 3. Concatenate Scenes

```bash
ffmpeg -y -f concat -safe 0 -i concat.txt \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  concatenated.mp4
```

### 4. Apply Fade Effects

```bash
TOTAL_DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 concatenated.mp4 | cut -d. -f1)
FADE_OUT_START=$((TOTAL_DURATION - 2))

ffmpeg -y -i concatenated.mp4 \
  -vf "fade=t=in:st=0:d=1.5,fade=t=out:st=${FADE_OUT_START}:d=2" \
  -af "afade=t=in:st=0:d=1.5,afade=t=out:st=${FADE_OUT_START}:d=2" \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  output/final.mp4
```

## Automated Assembly

The full process is automated in `scripts/assemble-video.sh`. Run:

```bash
bash scripts/assemble-video.sh \
  --script temp/script.json \
  --images temp/assets/images/ \
  --audio temp/assets/audio/ \
  --output output/
```
