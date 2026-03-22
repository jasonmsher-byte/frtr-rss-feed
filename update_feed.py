#!/usr/bin/env python3
"""
RSS Feed Updater for "From Rocks to Rockets" podcast.

Usage:
  python update_feed.py --add \
    --title "Episode Title" \
    --description "Episode description..." \
    --audio-url "https://..." \
    --audio-size 4793788 \
    --duration 388 \
    --episode-num 2 \
    --guid "frtr-2026-03-18-topic-slug" \
    --pub-date "Wed, 18 Mar 2026 08:00:00 -0400"

  python update_feed.py --set-base-url "https://your-site.github.io/frtr-rss-feed"
"""

import argparse
import os
import re
import sys
from datetime import datetime

FEED_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feed.xml")


def read_feed():
    with open(FEED_PATH, "r") as f:
        return f.read()


def write_feed(content):
    with open(FEED_PATH, "w") as f:
        f.write(content)
    print(f"Updated feed.xml ({len(content)} bytes)")


def set_base_url(base_url):
    """Replace placeholder URLs with the actual base URL."""
    content = read_feed()
    base_url = base_url.rstrip("/")
    
    # Replace cover image URL
    content = content.replace(
        'itunes:image href="PODCAST_COVER_URL"',
        f'itunes:image href="{base_url}/assets/cover.png"'
    )
    
    # Replace any remaining PODCAST_COVER_URL references
    content = content.replace("PODCAST_COVER_URL", f"{base_url}/assets/cover.png")
    
    # Replace episode audio URL placeholders
    content = content.replace("EPISODE_1_AUDIO_URL", f"{base_url}/assets/frtr-2026-03-17.mp3")
    
    # Add Atom self-link if not present
    if "atom:link" not in content:
        content = content.replace(
            "<language>en-us</language>",
            f'<atom:link href="{base_url}/feed.xml" rel="self" type="application/rss+xml"/>\n    <language>en-us</language>'
        )
    
    write_feed(content)
    print(f"Base URL set to: {base_url}")


def add_episode(title, description, audio_url, audio_size, duration, episode_num, guid, pub_date, episode_type="full"):
    """Add a new episode to the feed. episode_type can be 'full', 'trailer', or 'bonus'."""
    content = read_feed()
    
    # Build the new episode item
    # For trailers/clips, omit episode number so they don't mess up numbering
    episode_num_tag = f"\n      <itunes:episode>{episode_num}</itunes:episode>" if episode_type == "full" else ""
    item = f"""    <item>
      <title>{escape_xml(title)}</title>
      <description><![CDATA[{description}]]></description>
      <enclosure url="{audio_url}" length="{audio_size}" type="audio/mpeg"/>
      <guid isPermaLink="false">{guid}</guid>
      <pubDate>{pub_date}</pubDate>
      <itunes:duration>{duration}</itunes:duration>{episode_num_tag}
      <itunes:episodeType>{episode_type}</itunes:episodeType>
      <itunes:explicit>false</itunes:explicit>
    </item>
    <!-- EPISODES END -->"""
    
    # Insert before the EPISODES END marker
    content = content.replace("    <!-- EPISODES END -->", item)
    
    write_feed(content)
    print(f"Added episode {episode_num}: {title}")


def escape_xml(text):
    """Escape XML special characters."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text


def get_next_episode_number():
    """Count existing episodes and return the next number."""
    content = read_feed()
    count = content.count("<item>")
    return count + 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update FRTR podcast RSS feed")
    parser.add_argument("--add", action="store_true", help="Add a new episode")
    parser.add_argument("--set-base-url", type=str, help="Set the base URL for all assets")
    parser.add_argument("--title", type=str)
    parser.add_argument("--description", type=str)
    parser.add_argument("--audio-url", type=str)
    parser.add_argument("--audio-size", type=int)
    parser.add_argument("--duration", type=int, help="Duration in seconds")
    parser.add_argument("--episode-num", type=int)
    parser.add_argument("--guid", type=str)
    parser.add_argument("--pub-date", type=str)
    parser.add_argument("--episode-type", type=str, default="full", choices=["full", "trailer", "bonus"],
                        help="Episode type: full (default), trailer (for clips), or bonus")
    
    args = parser.parse_args()
    
    if args.set_base_url:
        set_base_url(args.set_base_url)
    
    if args.add:
        if not all([args.title, args.description, args.audio_url, args.audio_size, 
                     args.duration, args.guid, args.pub_date]):
            print("Error: --add requires --title, --description, --audio-url, --audio-size, --duration, --guid, --pub-date")
            sys.exit(1)
        ep_num = args.episode_num or get_next_episode_number()
        add_episode(args.title, args.description, args.audio_url, args.audio_size,
                    args.duration, ep_num, args.guid, args.pub_date, args.episode_type)
