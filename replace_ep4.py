#!/usr/bin/env python3
"""Replace Episode 4 (March 22) in feed.xml with the Terafab episode."""
import re

FEED_PATH = "/home/user/workspace/frtr-rss-feed/feed.xml"

with open(FEED_PATH, "r") as f:
    content = f.read()

# Find and replace the March 22 episode (The 48-Hour Ultimatum)
old_pattern = r'<item>\s*<title>The 48-Hour Ultimatum.*?</item>'
old_match = re.search(old_pattern, content, re.DOTALL)

if old_match:
    print(f"Found old Episode 4 at position {old_match.start()}-{old_match.end()}")
else:
    print("WARNING: Could not find old Episode 4 to replace")

new_item = """<item>
      <title>Musk&apos;s Terafab: The $25 Billion Bet to Build America&apos;s Chip Independence</title>
      <description><![CDATA[Last night Elon Musk formally announced the TERAFAB project -- a joint Tesla, SpaceX, and xAI venture to build the largest private semiconductor facility in American history. Located at the North Campus of Giga Texas in Austin, the Terafab targets over one terawatt of compute per year at 2-nanometer process technology. 80% of output is destined for space, 20% for ground. Jason Sher breaks down the announcement, the $25-45 billion price tag, the AI5 chip, ASML constraints, and what this means for US industrial independence. A solo episode.

Chapters:
0:00 Cold Open
0:10 Intro
0:30 The Announcement
1:30 Why Tesla Needs Its Own Fab
2:45 The Space Angle
3:45 Can They Actually Pull It Off?
5:00 What This Means for Reshoring
6:00 Outro

From Rocks to Rockets is AI-produced using our cloned voices. The research, the analysis, and the opinions are ours. Alera Group -- Emerging Industries.]]></description>
      <enclosure url="https://jasonmsher-byte.github.io/frtr-rss-feed/assets/frtr-2026-03-22.mp3" length="7277966" type="audio/mpeg"/>
      <guid isPermaLink="false">frtr-2026-03-22-musk-terafab</guid>
      <pubDate>Sun, 22 Mar 2026 09:00:00 -0400</pubDate>
      <itunes:duration>455</itunes:duration>
      <itunes:episode>4</itunes:episode>
      <itunes:episodeType>full</itunes:episodeType>
      <itunes:explicit>false</itunes:explicit>
    </item>"""

if old_match:
    content = content[:old_match.start()] + new_item + content[old_match.end():]
    with open(FEED_PATH, "w") as f:
        f.write(content)
    print("Replaced Episode 4 with Terafab episode")
else:
    # If no match, try inserting before EPISODES END
    insert_marker = "    <!-- EPISODES END -->"
    if insert_marker in content:
        content = content.replace(insert_marker, new_item + "\n    <!-- EPISODES END -->")
        with open(FEED_PATH, "w") as f:
            f.write(content)
        print("Inserted Terafab episode before EPISODES END marker")
    else:
        print("ERROR: Could not find insertion point")

# Verify
with open(FEED_PATH, "r") as f:
    final = f.read()
print(f"Feed size: {len(final)} bytes")
print(f"Episode count: {final.count('<item>')}")
assert "musk-terafab" in final, "Terafab GUID not found!"
print("Verification passed!")
