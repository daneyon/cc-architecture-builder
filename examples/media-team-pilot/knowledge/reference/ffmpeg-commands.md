# ffmpeg Command Reference

## Image Operations

### Scale to 1920x1080 with padding
```bash
ffmpeg -i input.png -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" output.png
```

### Ken Burns zoom-in effect
```bash
ffmpeg -loop 1 -i input.png -t 10 \
  -vf "zoompan=z='min(zoom+0.0015,1.5)':d=300:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30" \
  -c:v libx264 -pix_fmt yuv420p output.mp4
```

### Ken Burns pan (left to right)
```bash
ffmpeg -loop 1 -i input.png -t 10 \
  -vf "zoompan=z='1.3':d=300:x='if(eq(on,1),0,x+1)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30" \
  -c:v libx264 -pix_fmt yuv420p output.mp4
```

## Audio Operations

### Generate silence
```bash
ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 10 -c:a aac silence.m4a
```

### Generate low-volume sine wave (for placeholder audio)
```bash
ffmpeg -f lavfi -i "sine=frequency=440:duration=10" -af "volume=0.01" -c:a libmp3lame placeholder.mp3
```

### Concatenate audio files
```bash
ffmpeg -f concat -safe 0 -i audio_list.txt -c:a copy combined.mp3
```

## Video Composition

### Combine image video + audio
```bash
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -shortest output.mp4
```

### Concatenate video files
```bash
# Create list file:
# file 'scene_001.mp4'
# file 'scene_002.mp4'
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4
```

### Crossfade between two clips
```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "xfade=transition=fade:duration=1:offset=9" \
  output.mp4
```

## Effects

### Fade in/out
```bash
ffmpeg -i input.mp4 \
  -vf "fade=t=in:st=0:d=1.5,fade=t=out:st=58:d=2" \
  -af "afade=t=in:st=0:d=1.5,afade=t=out:st=58:d=2" \
  output.mp4
```

## Inspection

### Get video metadata (JSON)
```bash
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4
```

### Get duration only
```bash
ffprobe -v quiet -show_entries format=duration -of csv=p=0 input.mp4
```
