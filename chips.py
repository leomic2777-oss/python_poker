
import pygame as py


def get_visible_chips(balance, table_name):
    if table_name == "Vegas":

        if balance < 10_000:
            return 0, 0
        elif balance < 20_000:
            return 0, 2
        elif balance < 45_000:
            return 1, 4
        else:
            return 2, 4

    elif table_name == "Tokyo":

        if balance <= 0:
            return 0, 0
        elif balance < 100:
            return 0, 0
        elif balance < 200:
            return 0, 2
        elif balance < 450:
            return 1, 4
        else:
            return 2, 4

    return 0, 0


def draw_chips(screen, balance, table_name,
               red_chip_img, blue_chip_img):

    red_stacks, blue_stacks = get_visible_chips(
        balance, table_name
    )
    x = 1000
    y = 500
    for i in range(red_stacks):
        screen.blit(red_chip_img, (x, y))
        x += 55
    for i in range(blue_stacks):
        screen.blit(blue_chip_img, (x, y))
        x += 40
