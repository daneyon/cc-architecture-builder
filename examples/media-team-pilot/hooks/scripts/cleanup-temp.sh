#!/bin/bash
# cleanup-temp.sh
# Runs when the session stops (Stop hook)
# Optionally cleans up temporary files while preserving final output

TEMP_DIR="temp"

# Only clean up if a final video exists in output/
if ls output/*.mp4 1>/dev/null 2>&1; then
  echo "Final video exists in output/. Temp files can be safely cleaned up."
  echo "Run 'rm -rf temp/assets/' to free disk space."
else
  echo "No final video found. Preserving temp files for pipeline resume."
fi

# Always output valid JSON for hook system
cat <<EOF
{
  "continue": true,
  "message": "Session cleanup check complete"
}
EOF
