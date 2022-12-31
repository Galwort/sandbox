from ctypes import windll
from os import getcwd
from PIL import Image, ImageDraw
from random import randint

desk_rgb, gon_rgb, tow_rgb, gon2_rgb, tow2_rgb, colors, xy_map = ([] for i in range(7))

# iterating through rgb values for desk, gons, and towers
for i in range(3):
    desk_rgb.append(randint(10, 100))
    gon_rgb.append(desk_rgb[i] - 10)
    tow_rgb.append(max(0, gon_rgb[i] - 5))
    gon2_rgb.append(desk_rgb[i] + 20)
    tow2_rgb.append(gon2_rgb[i] - 5)

# converting rgb values to hex and appending to colors list
for i in (desk_rgb, gon_rgb, tow_rgb, gon2_rgb, tow2_rgb):
    colors.append("#%02x%02x%02x" % tuple(i))

# function to create and set desktop background
def create_desk(gon_sz=10):
    desk_x = windll.user32.GetSystemMetrics(0)
    desk_y = windll.user32.GetSystemMetrics(1)

    # creating list of coordinates for the hexagons
    def create_map(gon_sz=gon_sz):
        x, y = gon_sz * 8, 0
        i = 0

        while y <= desk_y:
            while x <= desk_x:
                xy_map.append((i, x, y))
                x += gon_sz * 24
                i += 1
            y += gon_sz * 14
            x = gon_sz * 8
            i += (desk_x // (gon_sz * 24))

        x, y = gon_sz * 20, gon_sz * 7
        i = desk_x // (gon_sz * 24)
        while y <= desk_y:
            while x <= desk_x:
                xy_map.append((i, x, y))
                x += gon_sz * 24
                i += 1
            y += gon_sz * 14
            x = gon_sz * 20
            i += (desk_x // (gon_sz * 24))
        xy_map.sort(key=lambda x: x[0])
    create_map()

    desk_im = Image.new("RGB", (desk_x, desk_y), colors[0])
    desk_draw = ImageDraw.Draw(desk_im)

    # randomly placing gons at coordinates in xy_map
    def create_gons(towers=True):
        gon = 0
        while gon < len(xy_map):
            x = xy_map[gon][1]
            y = xy_map[gon][2]
            gon_color, tow_color = (
                (colors[1], colors[2]) if randint(0, 2) == 0 else (colors[3], colors[4])
            )

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
            gon += randint(1, 3)

    create_gons()
    desk_im.save("causeway.png")


create_desk()
windll.user32.SystemParametersInfoW(20, 0, getcwd() + r"\causeway.png", 0)
