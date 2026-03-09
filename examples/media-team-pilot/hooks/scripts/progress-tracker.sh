#!/bin/bash
# progress-tracker.sh
# Runs after each subagent completes (SubagentStop hook)
# Tracks pipeline progress by checking which artifacts exist

TEMP_DIR="temp"
OUTPUT_DIR="output"
PROGRESS_FILE="temp/pipeline-progress.json"

# Initialize progress tracking
declare -A steps
steps=(
  ["research"]="temp/research-brief.md"
  ["script"]="temp/script.json"
  ["image_prompts"]="temp/image-prompts.json"
  ["images"]="temp/assets/images"
  ["audio"]="temp/assets/audio"
  ["video"]="output/*.mp4"
  ["metadata"]="output/metadata.json"
)

completed=0
total=${#steps[@]}

for step in "${!steps[@]}"; do
  path="${steps[$step]}"
  if [[ -e $path ]] || ls $path 1>/dev/null 2>&1; then
    completed=$((completed + 1))
  fi
done

# Write progress as JSON to stdout (hook output)
cat <<EOF
{
  "continue": true,
  "message": "Pipeline progress: ${completed}/${total} steps completed"
}
EOF
