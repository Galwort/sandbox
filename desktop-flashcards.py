from ctypes import windll
from os import getcwd
from PIL import Image, ImageDraw, ImageFont
from random import choice, randint
from textwrap import wrap

desk_rgb, card_rgb, outline_rgb, colors = [], [], [], []

for i in range(3):
    desk_rgb.append(randint(0, 50))
    card_rgb.append(desk_rgb[i] + 20)
    outline_rgb.append(desk_rgb[i] + 10)

for x in (desk_rgb, card_rgb, outline_rgb):
    colors.append('#%02x%02x%02x' % tuple(x))

desk_x = windll.user32.GetSystemMetrics(0)
desk_y = windll.user32.GetSystemMetrics(1)

desk_im = Image.new('RGB', (desk_x, desk_y), colors[0])
desk_draw = ImageDraw.Draw(desk_im)
card_font = ImageFont.truetype('calibri.ttf', int(desk_y / 25))

with open('flashcards.txt') as f:
    lines = f.readlines()

line = choice(lines).strip()
card_text = '\n'.join(wrap(line, 50))
_, _, w, h = desk_draw.multiline_textbbox((0,0), card_text, card_font, spacing=20)

desk_draw.rounded_rectangle((int(desk_x / 2 - (w + 100) / 2),
                            int(desk_y / 2 - (h + 100) / 2),
                            int(desk_x / 2 + (w + 100) / 2),
                            int(desk_y / 2 + (h + 100) / 2)),
                            50,
                            colors[1],
                            colors[2],
                            3)

desk_draw.text(((desk_x - w)/2,
                (desk_y - h)/2),
                card_text,
                fill='white',
                font=card_font,
                spacing=20,
                align='center')

desk_im.save("flashcard.png")
windll.user32.SystemParametersInfoW(20,
                                    0,
                                    getcwd() + r"\flashcard.png",
                                    0)