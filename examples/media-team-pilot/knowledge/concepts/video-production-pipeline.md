# Video Production Pipeline

## Overview

The media team pilot follows a 6-stage sequential pipeline where each stage produces file artifacts consumed by the next. This mirrors professional video production workflows (pre-production → production → post-production) mapped to AI agent specializations.

## Pipeline Stages

```
Creative Brief → Research → Script → Visual Design → Media Generation → Assembly → Review
```

### Stage 1: Research (Pre-Production)
- **Agent**: research-agent
- **Input**: User's creative brief (natural language)
- **Output**: `temp/research-brief.md`
- **Purpose**: Gather context, references, and creative direction to inform the script

### Stage 2: Scriptwriting (Pre-Production)
- **Agent**: scriptwriter
- **Input**: Research brief + original prompt
- **Output**: `temp/script.json`
- **Purpose**: Create the scene-by-scene blueprint with narration and visual descriptions

### Stage 3: Visual Design (Pre-Production)
- **Agent**: visual-designer
- **Input**: Script JSON
- **Output**: `temp/image-prompts.json`
- **Purpose**: Optimize scene descriptions into image generation prompts with visual consistency

### Stage 4: Media Generation (Production)
- **Agent**: media-producer
- **Input**: Image prompts + script narration
- **Output**: `temp/assets/images/*.png` + `temp/assets/audio/*.mp3`
- **Purpose**: Execute API calls to generate the actual visual and audio assets

### Stage 5: Video Assembly (Post-Production)
- **Agent**: video-assembler
- **Input**: Asset files + script timing
- **Output**: `output/<video-name>.mp4`
- **Purpose**: Combine images + audio into final video with effects and transitions

### Stage 6: Quality Review (Post-Production)
- **Agent**: quality-reviewer
- **Input**: Final video + script
- **Output**: `output/metadata.json` + review summary
- **Purpose**: Validate output quality and prepare publishing metadata

## Key Principles

1. **File-based handoff**: Each agent communicates through files in `temp/`, not shared memory
2. **Sequential dependencies**: Each stage requires the previous stage's output
3. **Fail-fast**: Pipeline stops on any stage failure rather than proceeding with missing assets
4. **Idempotent stages**: Any stage can be re-run independently to regenerate its output
