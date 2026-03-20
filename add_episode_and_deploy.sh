#!/bin/bash
# Add a new episode to the RSS feed and push to GitHub Pages
# Called by the daily cron after uploading to YouTube and Drive
#
# Usage: bash add_episode_and_deploy.sh \
#   --title "Episode Title" \
#   --description "Full description with chapters..." \
#   --audio-file "/path/to/episode.mp3" \
#   --duration 388 \
#   --guid "frtr-2026-03-18-topic-slug" \
#   --pub-date "Wed, 18 Mar 2026 08:00:00 -0400"

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --title) TITLE="$2"; shift 2 ;;
        --description) DESCRIPTION="$2"; shift 2 ;;
        --audio-file) AUDIO_FILE="$2"; shift 2 ;;
        --duration) DURATION="$2"; shift 2 ;;
        --guid) GUID="$2"; shift 2 ;;
        --pub-date) PUB_DATE="$2"; shift 2 ;;
        --episode-num) EPISODE_NUM="$2"; shift 2 ;;
        *) echo "Unknown arg: $1"; shift ;;
    esac
done

# Get GitHub username and base URL
GH_USER=$(gh api user --jq '.login')
REPO_NAME="frtr-rss-feed"
BASE_URL="https://${GH_USER}.github.io/${REPO_NAME}"

# Extract date from guid for filename
AUDIO_BASENAME=$(basename "$AUDIO_FILE")
DEST_NAME="$AUDIO_BASENAME"

# Copy audio file to assets
echo "Copying audio to assets..."
cp "$AUDIO_FILE" "assets/${DEST_NAME}"
AUDIO_SIZE=$(stat -f%z "assets/${DEST_NAME}" 2>/dev/null || stat -c%s "assets/${DEST_NAME}")
AUDIO_URL="${BASE_URL}/assets/${DEST_NAME}"

echo "Audio: ${AUDIO_URL} (${AUDIO_SIZE} bytes)"

# Add episode to feed
python3 update_feed.py --add \
    --title "$TITLE" \
    --description "$DESCRIPTION" \
    --audio-url "$AUDIO_URL" \
    --audio-size "$AUDIO_SIZE" \
    --duration "$DURATION" \
    --guid "$GUID" \
    --pub-date "$PUB_DATE" \
    ${EPISODE_NUM:+--episode-num "$EPISODE_NUM"}

# Commit and push
git add -A
git commit -m "Add episode: ${TITLE}" 2>/dev/null || echo "No changes to commit"
git push origin main 2>/dev/null || git push origin master

echo ""
echo "Episode added and deployed."
echo "Feed URL: ${BASE_URL}/feed.xml"
echo "Audio URL: ${AUDIO_URL}"
