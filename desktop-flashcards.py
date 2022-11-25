from ctypes import windll
from random import choice
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap

desk_x = windll.user32.GetSystemMetrics(0)
desk_y = windll.user32.GetSystemMetrics(1)

desk_im = Image.new('RGB', (desk_x, desk_y))
desk_draw = ImageDraw.Draw(desk_im)
card_font = ImageFont.truetype('arial.ttf', desk_y//25)

with open('flashcards.txt') as f:
    lines = f.readlines()
    line = choice(lines).strip()
    card_text = wrap(line, 10)
    desk_draw.text((desk_x//2 - desk_draw.textbbox((0,0), card_text, card_font)[0]//2,
                    desk_y//2 - desk_draw.textbbox((0,0), card_text, card_font)[1]//2),
                    card_text,
                    fill='white',
                    font=card_font,
                    align='center')
    desk_im.show()

# import textwrap
# lines = textwrap.wrap(text, width=40)
# y_text = h
# for line in lines:
#     width, height = font.getsize(line)
#     draw.text(((w - width) / 2, y_text), line, font=font, fill=FOREGROUND)
#     y_text += height