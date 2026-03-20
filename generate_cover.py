"""Generate square podcast cover art (1400x1400) for RSS/Spotify/iTunes."""
from PIL import Image, ImageDraw, ImageFont
import os

SIZE = 1400
img = Image.new('RGB', (SIZE, SIZE), '#0a0a0f')
draw = ImageDraw.Draw(img)

# Dark gradient background with subtle texture
for y in range(SIZE):
    r = int(10 + (y / SIZE) * 12)
    g = int(10 + (y / SIZE) * 10)
    b = int(15 + (y / SIZE) * 20)
    draw.line([(0, y), (SIZE, y)], fill=(r, g, b))

# Accent line at top
draw.rectangle([(0, 0), (SIZE, 6)], fill='#00d4aa')

# Subtle grid pattern
for x in range(0, SIZE, 70):
    draw.line([(x, 0), (x, SIZE)], fill=(255, 255, 255, 8), width=1)
for y in range(0, SIZE, 70):
    draw.line([(0, y), (SIZE, y)], fill=(255, 255, 255, 8), width=1)

# Try to load fonts
def get_font(size, bold=False):
    font_paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

# "FROM ROCKS" text
font_title = get_font(120, bold=True)
font_to = get_font(60, bold=False)
font_subtitle = get_font(120, bold=True)
font_byline = get_font(38, bold=False)
font_tagline = get_font(28, bold=False)

# Layout from top
y_start = 280

# "FROM ROCKS"
text1 = "FROM ROCKS"
bbox1 = draw.textbbox((0, 0), text1, font=font_title)
w1 = bbox1[2] - bbox1[0]
draw.text(((SIZE - w1) // 2, y_start), text1, fill='#ffffff', font=font_title)

# "TO"
text_to = "TO"
bbox_to = draw.textbbox((0, 0), text_to, font=font_to)
w_to = bbox_to[2] - bbox_to[0]
draw.text(((SIZE - w_to) // 2, y_start + 130), text_to, fill='#00d4aa', font=font_to)

# "ROCKETS"
text2 = "ROCKETS"
bbox2 = draw.textbbox((0, 0), text2, font=font_subtitle)
w2 = bbox2[2] - bbox2[0]
draw.text(((SIZE - w2) // 2, y_start + 200), text2, fill='#ffffff', font=font_subtitle)

# Accent underline below ROCKETS
line_y = y_start + 330
draw.rectangle([(SIZE//2 - 200, line_y), (SIZE//2 + 200, line_y + 3)], fill='#00d4aa')

# "by ALERA GROUP"
byline = "by ALERA GROUP"
bbox_by = draw.textbbox((0, 0), byline, font=font_byline)
w_by = bbox_by[2] - bbox_by[0]
draw.text(((SIZE - w_by) // 2, y_start + 360), byline, fill='#8a8a9a', font=font_byline)

# Tagline at bottom
tagline = "THE INDUSTRIES BUILDING THE FUTURE"
bbox_tag = draw.textbbox((0, 0), tagline, font=font_tagline)
w_tag = bbox_tag[2] - bbox_tag[0]
draw.text(((SIZE - w_tag) // 2, SIZE - 120), tagline, fill='#5a5a6a', font=font_tagline)

# Bottom accent line
draw.rectangle([(0, SIZE - 6), (SIZE, SIZE)], fill='#00d4aa')

# Save
output_path = '/home/user/workspace/frtr-rss-feed/assets/cover.png'
img.save(output_path, 'PNG', quality=95)
print(f"Cover art saved: {output_path}")
print(f"Size: {os.path.getsize(output_path)} bytes")
