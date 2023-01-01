from ctypes import windll
from os import getcwd
from PIL import Image, ImageDraw
from random import randint

desk_rgb = []

for i in range(3):
    desk_rgb.append(randint(10, 100))

desk_color = "#%02x%02x%02x" % tuple(desk_rgb)

accent_rgb = []

for i in range(3):
    accent_rgb.append(randint(50, 150))

accent_color = "#%02x%02x%02x" % tuple(accent_rgb)

# creating random colors for gons and towers based on desk color
def create_colors(desk_rgb=desk_rgb):
    gon_rgb, tow_rgb = ([] for i in range(2))
    ri = randint(-10, 10)
    op_rgb = accent_rgb if randint(0,5) == 0 else desk_rgb
    for i in range(3):
        gon_rgb.append(op_rgb[i] + ri)
        tow_rgb.append(max(0, gon_rgb[i] - 5))

    gon_color = "#%02x%02x%02x" % tuple(gon_rgb)
    tow_color = "#%02x%02x%02x" % tuple(tow_rgb)
    return gon_color, tow_color


# function to create and set desktop background
def create_desk(gon_sz=10):
    desk_x = windll.user32.GetSystemMetrics(0)
    desk_y = windll.user32.GetSystemMetrics(1)

    # creating list of coordinates for the hexagons
    def create_map(gon_sz=gon_sz):
        xy_map = []
        x, y = gon_sz * 8, 0
        i = 0

        while y <= desk_y:
            while x <= desk_x:
                xy_map.append((i, x, y))
                x += gon_sz * 24
                i += 1
            y += gon_sz * 14
            x = gon_sz * 8
            i += desk_x // (gon_sz * 24)

        x, y = gon_sz * 20, gon_sz * 7
        i = desk_x // (gon_sz * 24)
        while y <= desk_y:
            while x <= desk_x:
                xy_map.append((i, x, y))
                x += gon_sz * 24
                i += 1
            y += gon_sz * 14
            x = gon_sz * 20
            i += desk_x // (gon_sz * 24)
        xy_map.sort(key=lambda x: x[0])
        return xy_map
    create_map()

    desk_im = Image.new("RGB", (desk_x, desk_y), desk_color)
    desk_draw = ImageDraw.Draw(desk_im)

    # randomly placing gons at coordinates in xy_map
    def create_gons(towers=True):
        xy_map = create_map()
        gon = 0
        while gon < len(xy_map):
            x = xy_map[gon][1]
            y = xy_map[gon][2]
            gon_color, tow_color = create_colors()

            desk_draw.polygon(
                [
                    (x - 4 * gon_sz, y + 7 * gon_sz),  # bottom left
                    (x + 4 * gon_sz, y + 7 * gon_sz),  # bottom right
                    (x + 8 * gon_sz, y),  # right
                    (x + 4 * gon_sz, y - 7 * gon_sz),  # top right
                    (x - 4 * gon_sz, y - 7 * gon_sz),  # top left
                    (x - 8 * gon_sz, y),  # left
                ],
                fill=gon_color,
            )

            if towers == True:
                tow_h = randint(1, 3) / 4
                desk_draw.polygon(
                    [
                        (x + 8 * gon_sz, y),  # top right
                        (x + 4 * gon_sz, y + 7 * gon_sz),  # top middle right
                        (x - 4 * gon_sz, y + 7 * gon_sz),  # top middle left
                        (x - 8 * gon_sz, y),  # top left
                        (x - 8 * gon_sz, y + (14 * gon_sz * tow_h)),  # bottom left
                        (
                            x - 4 * gon_sz,
                            y + (14 * gon_sz * tow_h) + 7 * gon_sz,
                        ),  # bottom middle left
                        (
                            x + 4 * gon_sz,
                            y + (14 * gon_sz * tow_h) + 7 * gon_sz,
                        ),  # bottom middle right
                        (x + 8 * gon_sz, y + (14 * gon_sz * tow_h)),  # bottom right
                    ],
                    fill=tow_color,
                )
            gon += randint(1, 2)

    create_gons()
    desk_im.save("causeway.png")


create_desk()
windll.user32.SystemParametersInfoW(20, 0, getcwd() + r"\causeway.png", 0)
