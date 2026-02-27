---
description: Create a narrative video from a creative brief — orchestrates the full multi-agent pipeline
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
thinking: extended
---

# Create Video

Produce a complete narrative slideshow video (.mp4) from the user's creative brief by orchestrating the full agent pipeline.

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `$ARGUMENTS` | Yes | The creative brief describing the video to produce |

## Behavior

Execute the video production pipeline sequentially. Each step uses a specialized agent that produces file artifacts consumed by the next step.

**IMPORTANT**: Before starting, ensure the working environment is ready:
1. Create `temp/` and `temp/assets/images/` and `temp/assets/audio/` directories
2. Check that `providers/config.json` exists (if not, create one with `placeholder` defaults)
3. Verify ffmpeg is available: `which ffmpeg`

## Pipeline Steps

### Step 1: Research
Use the **research-agent** to gather context and inspiration.
- Input: The user's creative brief ($ARGUMENTS)
- Output: `temp/research-brief.md`

### Step 2: Script Writing
Use the **scriptwriter** agent to create the scene-by-scene script.
- Input: `temp/research-brief.md` + original brief
- Tell the agent: "Read temp/research-brief.md for context. The user's creative brief is: $ARGUMENTS"
- Output: `temp/script.json`

### Step 3: Visual Design
Use the **visual-designer** agent to create image generation prompts.
- Input: `temp/script.json`
- Tell the agent: "Read temp/script.json and create optimized image prompts for each scene"
- Output: `temp/image-prompts.json`

### Step 4: Media Production
Use the **media-producer** agent to generate images and audio.
- Input: `temp/image-prompts.json` + `temp/script.json`
- Tell the agent: "Generate images from temp/image-prompts.json and audio from temp/script.json narration"
- Output: `temp/assets/images/scene_NNN.png` + `temp/assets/audio/scene_NNN.mp3`

### Step 5: Video Assembly
Use the **video-assembler** agent to combine assets into .mp4.
- Input: `temp/assets/` + `temp/script.json`
- Tell the agent: "Assemble the video from assets in temp/assets/ using timing from temp/script.json"
- Output: `output/<video-name>.mp4`

### Step 6: Quality Review
Use the **quality-reviewer** agent to validate and generate metadata.
- Input: `output/<video-name>.mp4` + `temp/script.json`
- Tell the agent: "Review the video in output/ and generate metadata"
- Output: `output/metadata.json` + review summary

## After Pipeline Completes

Present the user with:
- Final video file path and size
- Video duration and scene count
- Quality review summary
- Any warnings or suggestions
- Instructions for `/publish-video` if they want to upload

## Error Handling

If any step fails:
- Stop the pipeline
- Report which step failed and why
- Suggest specific remediation (e.g., "Image generation failed for scenes 3 and 7 — try re-running media-producer for those scenes")
- Do NOT continue to the next step with missing assets
