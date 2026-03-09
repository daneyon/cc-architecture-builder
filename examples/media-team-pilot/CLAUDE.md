# Media Team Pilot

> Multi-agent creative team that produces narrative slideshow videos (.mp4) from a single prompt.

## Purpose

This plugin orchestrates a team of specialized agents to transform a creative brief into a complete video with narration, visuals, and metadata — ready for YouTube upload. The pipeline follows a sequential chain pattern where each agent produces file artifacts consumed by the next.

## Domain

Creative media production: storytelling videos with AI-generated visuals, text-to-speech narration, and ffmpeg-based video assembly.

## Knowledge Base

Domain knowledge is organized in `knowledge/`:

- `knowledge/INDEX.md` — Master catalog of all knowledge files
- `knowledge/concepts/` — Video production pipeline, storytelling structure
- `knowledge/procedures/` — ffmpeg assembly, provider configuration
- `knowledge/reference/` — ffmpeg commands, API providers, video specs
- `knowledge/examples/` — Sample creative briefs

For domain questions, first consult `knowledge/INDEX.md` to identify relevant files.

## Available Commands

| Command | Description |
|---------|-------------|
| `/create-video` | Create a video from a creative brief (orchestrates full pipeline) |
| `/review-video` | Review an existing video output and suggest improvements |
| `/publish-video` | Prepare or upload video to a platform like YouTube |

## Specialized Agents

| Agent | Use When |
|-------|----------|
| `research-agent` | Gathering reference material and context for a creative brief |
| `scriptwriter` | Writing the video script with scene breakdowns and narration |
| `visual-designer` | Creating optimized image generation prompts from scene descriptions |
| `media-producer` | Executing API calls to generate images and audio assets |
| `video-assembler` | Combining assets into final .mp4 via ffmpeg |
| `quality-reviewer` | Validating output quality and generating metadata |

## Video Production Pipeline

When `/create-video` is invoked with a creative brief, execute this pipeline **sequentially**. Each agent writes artifacts to `temp/` that the next agent consumes. Pass relevant file paths explicitly between agents.

```
Step 1: research-agent
  Input:  User's creative brief
  Output: temp/research-brief.md

Step 2: scriptwriter
  Input:  temp/research-brief.md + user's original brief
  Output: temp/script.json

Step 3: visual-designer
  Input:  temp/script.json
  Output: temp/image-prompts.json

Step 4: media-producer
  Input:  temp/image-prompts.json + temp/script.json (for narration text)
  Output: temp/assets/images/*.png + temp/assets/audio/*.mp3

Step 5: video-assembler
  Input:  temp/assets/ + temp/script.json (for timing)
  Output: output/<project-name>.mp4

Step 6: quality-reviewer
  Input:  output/<project-name>.mp4 + temp/script.json
  Output: output/metadata.json + review summary to user
```

### Context Handoff Rules

- Always tell the next agent which files to read from `temp/`
- Include the user's original creative brief when invoking scriptwriter
- After media-producer completes, verify asset counts match script scene count before proceeding to assembler
- If any agent reports an error, stop the pipeline and report to the user with suggested remediation

### Provider Configuration

External API providers are configured in `providers/config.json`. The active providers determine which image generation and TTS services are used. Placeholder providers are available for testing without API keys.

Before running the media-producer agent, verify that `providers/config.json` exists and has valid provider selections. If no config exists, default to `placeholder` providers for both image and TTS.

## Script Format

All agents producing or consuming the script must use this JSON structure:

```json
{
  "title": "Video Title",
  "description": "Brief description",
  "total_duration_seconds": 120,
  "scenes": [
    {
      "scene_number": 1,
      "duration_seconds": 10,
      "narration": "Text spoken during this scene",
      "visual_description": "What the viewer sees",
      "transition": "crossfade",
      "notes": "Optional production notes"
    }
  ],
  "style": {
    "visual_tone": "cinematic, warm",
    "narration_voice": "calm, storytelling",
    "music_mood": "ambient, gentle"
  }
}
```

## Constraints

- All generated assets go to `temp/` (gitignored, disposable)
- Final deliverables go to `output/` (video + metadata)
- Never hardcode API keys — use environment variables or `providers/config.local.json`
- ffmpeg must be available in PATH for video assembly
- Python 3.8+ required for provider scripts
- Maximum 20 scenes per video (practical limit for slideshow format)
- Target output: 1920x1080, 30fps, H.264 codec

## Output Guidelines

Final video output should include:
- `output/<project-name>.mp4` — The video file
- `output/metadata.json` — Title, description, tags, thumbnail timestamp
- Summary report to the user with: duration, scene count, file size, and any warnings
