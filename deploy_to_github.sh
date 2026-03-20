#!/bin/bash
# Deploy RSS feed to GitHub Pages
# Usage: bash deploy_to_github.sh [github_username]
# 
# This script:
# 1. Creates the repo on GitHub (if it doesn't exist)
# 2. Pushes the feed + assets
# 3. Enables GitHub Pages
# 4. Your RSS feed will be at: https://<username>.github.io/frtr-rss-feed/feed.xml

set -e

REPO_NAME="frtr-rss-feed"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

# Check if repo exists, create if not
if ! gh repo view "$REPO_NAME" &>/dev/null; then
    echo "Creating GitHub repo: $REPO_NAME"
    gh repo create "$REPO_NAME" --public --description "From Rocks to Rockets Podcast RSS Feed" --source . --push
else
    echo "Repo $REPO_NAME already exists"
fi

# Get the GitHub username
GH_USER=$(gh api user --jq '.login')
BASE_URL="https://${GH_USER}.github.io/${REPO_NAME}"

echo "Setting base URL to: $BASE_URL"
python3 update_feed.py --set-base-url "$BASE_URL"

# Commit and push
git add -A
git commit -m "Update RSS feed $(date +%Y-%m-%d)" 2>/dev/null || echo "No changes to commit"
git push origin main 2>/dev/null || git push origin master 2>/dev/null || {
    git branch -M main
    git push -u origin main
}

# Enable GitHub Pages on the main branch
echo "Enabling GitHub Pages..."
gh api repos/${GH_USER}/${REPO_NAME}/pages \
    --method POST \
    --field "source[branch]=main" \
    --field "source[path]=/" 2>/dev/null || \
gh api repos/${GH_USER}/${REPO_NAME}/pages \
    --method PUT \
    --field "source[branch]=main" \
    --field "source[path]=/" 2>/dev/null || \
echo "GitHub Pages may already be enabled"

echo ""
echo "============================================"
echo "RSS Feed URL: ${BASE_URL}/feed.xml"
echo "Landing Page: ${BASE_URL}/"
echo "============================================"
echo ""
echo "Submit this RSS URL to Spotify for Creators:"
echo "  ${BASE_URL}/feed.xml"
