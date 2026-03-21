#!/usr/bin/env python3
"""Replace Episode 3 in feed.xml with the correct semiconductor episode."""

import re

FEED_PATH = "/home/user/workspace/frtr-rss-feed/feed.xml"

with open(FEED_PATH, "r") as f:
    content = f.read()

# The old Episode 3 item to replace
old_item_pattern = r'<item>\s*<title>AI Just Hit a Wall.*?</item>'
old_match = re.search(old_item_pattern, content, re.DOTALL)

if old_match:
    print(f"Found old Episode 3 at position {old_match.start()}-{old_match.end()}")
else:
    print("WARNING: Could not find old Episode 3 to replace")

new_item = """<item>
      <title>America&apos;s Chip Comeback: Intel, AMD, and the Race to Build Semiconductors on U.S. Soil</title>
      <description><![CDATA[The most advanced semiconductor ever manufactured on American soil just shipped — from Intel's Fab 52 in Chandler, Arizona. Meanwhile, AMD and Flex are assembling the most powerful AI GPU platforms in Austin, Texas. In this episode, Jason Sher and Shane Smith break down the U.S. semiconductor renaissance — Intel's 18A breakthrough, the $19 billion in CHIPS Act funding backing it, AMD's new GPU assembly line, and why geographic diversity away from Taiwan is now a competitive advantage for the entire data center industry.

Chapters:
0:00 Cold Open
0:08 Intro
0:30 Intel's 18A Breakthrough
1:20 Panther Lake and Fab 52
2:15 AMD and Flex in Austin
3:10 CHIPS Act and the Money Behind It
4:05 The Taiwan Risk
4:55 What This Means for Data Centers
5:40 Outro

From Rocks to Rockets is AI-produced using our cloned voices. The research, the analysis, and the opinions are ours. Alera Group — Emerging Industries.]]></description>
      <enclosure url="https://jasonmsher-byte.github.io/frtr-rss-feed/assets/frtr-2026-03-21.mp3" length="7551066" type="audio/mpeg"/>
      <guid isPermaLink="false">frtr-2026-03-21-semiconductor-comeback</guid>
      <pubDate>Sat, 21 Mar 2026 08:00:00 -0400</pubDate>
      <itunes:duration>510</itunes:duration>
      <itunes:episode>3</itunes:episode>
      <itunes:episodeType>full</itunes:episodeType>
      <itunes:explicit>false</itunes:explicit>
    </item>"""

if old_match:
    content = content[:old_match.start()] + new_item + content[old_match.end():]
    with open(FEED_PATH, "w") as f:
        f.write(content)
    print("Successfully replaced Episode 3 in feed.xml")
else:
    print("No replacement made")

# Verify
with open(FEED_PATH, "r") as f:
    final = f.read()
print(f"\nFeed size: {len(final)} bytes")
print(f"Episode count: {final.count('<item>')}")
assert "semiconductor-comeback" in final, "New GUID not found!"
assert "AI Just Hit a Wall" not in final, "Old episode still present!"
print("Verification passed!")
