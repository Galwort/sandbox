from ctypes import windll
from os import getcwd
from PIL import Image, ImageDraw, ImageFont
from random import choice, randint
from textwrap import wrap

def rgb_to_hex(red, green, blue):
    return '#%02x%02x%02x' % (red, green, blue)

desk_r = randint(0,50)
desk_g = randint(0,50)
desk_b = randint(0,50)

card_r = desk_r + 20
card_g = desk_g + 20
card_b = desk_b + 20

outline_r = desk_r + 10
outline_g = desk_g + 10
outline_b = desk_b + 10

desk_color = rgb_to_hex(desk_r, desk_g, desk_b)
card_color = rgb_to_hex(card_r, card_g, card_b)
outline_color = rgb_to_hex(outline_r, outline_g, outline_b)

desk_x = windll.user32.GetSystemMetrics(0)
desk_y = windll.user32.GetSystemMetrics(1)

desk_im = Image.new('RGB', (desk_x, desk_y), desk_color)
desk_draw = ImageDraw.Draw(desk_im)
card_font = ImageFont.truetype('calibri.ttf', int(desk_y / 25))

with open('flashcards.txt') as f:
    lines = f.readlines()

line = choice(lines).strip()
card_text = '\n'.join(wrap(line, 50))
_, _, w, h = desk_draw.multiline_textbbox((0,0), card_text, card_font, spacing=20)

card_width = 1000
card_height = 200

desk_draw.rounded_rectangle((int(desk_x / 2 - (w + 100) / 2),
                            int(desk_y / 2 - (h + 100) / 2),
                            int(desk_x / 2 + (w + 100) / 2),
                            int(desk_y / 2 + (h + 100) / 2)),
                            50,
                            card_color,
                            outline_color,
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