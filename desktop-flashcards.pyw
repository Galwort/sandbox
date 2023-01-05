from ctypes import windll
from os import getcwd
from PIL import Image, ImageDraw, ImageFont
from random import choice, randint
from textwrap import wrap

desk_rgb, card_rgb, outline_rgb, gon_rgb, colors, xy_map = ([] for i in range(6))

for i in range(3):
    desk_rgb.append(randint(0, 50))
    card_rgb.append(desk_rgb[i] + 20)
    outline_rgb.append(desk_rgb[i] + 10)
    gon_rgb.append(max(0, desk_rgb[i] - 10))

for i in (desk_rgb, card_rgb, outline_rgb, gon_rgb):
    colors.append("#%02x%02x%02x" % tuple(i))

desk_x = windll.user32.GetSystemMetrics(0)
desk_y = windll.user32.GetSystemMetrics(1)

x, y = 80, 0
while x <= desk_x:
    while y <= desk_y:
        xy_map.append((x, y))
        y += 140
    x += 240
    y = 0

x, y = 200, 70
while x <= desk_x:
    while y <= desk_y:
        xy_map.append((x, y))
        y += 140
    x += 240
    y = 70

desk_im = Image.new("RGB", (desk_x, desk_y), colors[0])
desk_draw = ImageDraw.Draw(desk_im)
card_font = ImageFont.truetype("arial.ttf", int(desk_y / 25))

for i in range(randint(20, 50)):
    gon = randint(0, len(xy_map) - 1)
    x = xy_map[gon][0]
    y = xy_map[gon][1]
    gon_color = colors[2] if randint(0, 2) == 0 else colors[3]
    desk_draw.polygon(
        [
            (x - 40, y + 70),
            (x + 40, y + 70),
            (x + 80, y),
            (x + 40, y - 70),
            (x - 40, y - 70),
            (x - 80, y),
        ],
        fill=gon_color,
    )
    i += 1

with open("flashcards.txt") as f:
    lines = f.readlines()

line = choice(lines).strip()
card_text = "\n".join(wrap(line, 50))
_, _, w, h = desk_draw.multiline_textbbox((0, 0), card_text, card_font, spacing=20)

desk_draw.rounded_rectangle(
    (
        int(desk_x / 2 - (w + 100) / 2),
        int(desk_y / 2 - (h + 100) / 2),
        int(desk_x / 2 + (w + 100) / 2),
        int(desk_y / 2 + (h + 100) / 2),
    ),
    50,
    colors[1],
    colors[2],
    3,
)

desk_draw.text(
    ((desk_x - w) / 2, (desk_y - h) / 2),
    card_text,
    fill="white",
    font=card_font,
    spacing=20,
    align="center",
)

desk_im.save("flashcard.png")
windll.user32.SystemParametersInfoW(20, 0, getcwd() + r"\flashcard.png", 0)
