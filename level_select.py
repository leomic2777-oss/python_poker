
import pygame as py

py.init()
WIDTH = 1280
HEIGHT = 680

screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Poker Game")

BG = (11, 20, 16)
CARD_BG = (23, 37, 29)
GOLD = (214, 182, 110)
LIGHT_GOLD = (232, 205, 140)
WHITE = (255, 255, 255)
GREEN = (23, 74, 53)

title_font = py.font.SysFont("georgia", 36, bold=True)
name_font = py.font.SysFont("georgia", 27, bold=True)
body_font = py.font.SysFont("arial", 18)
button_font = py.font.SysFont("georgia", 17, bold=True)

vegas_img = py.image.load("vegaslevel.png").convert()
tokyo_img = py.image.load("tokyolevel.png").convert()
vegas_img = py.transform.smoothscale(vegas_img, (520, 250))
tokyo_img = py.transform.smoothscale(tokyo_img, (520, 250))

vegas_card = py.Rect(50, 165, 550, 440)
tokyo_card = py.Rect(680, 165, 550, 440)

vegas_button = py.Rect(195, 535, 260, 45)
tokyo_button = py.Rect(825, 535, 260, 45)
back_button = py.Rect(35, 615, 150, 45)


def draw_text(text, font, colour, x, y, center=True):
    image = font.render(text, True, colour)
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(image, rect)


def draw_card(card, image, name, description, button, mouse_pos):
    py.draw.rect(screen, CARD_BG, card, border_radius=8)
    py.draw.rect(screen, GOLD, card, 2, border_radius=8)
    screen.blit(image, (card.x + 15, card.y + 15))

    draw_text(name, name_font, GOLD, card.centerx, card.y + 290)
    lines = description.split("|")

    for i, line in enumerate(lines):
        draw_text(line, body_font, WHITE, card.centerx, card.y + 330 + i * 25
                  )

    button_colour = (
        LIGHT_GOLD if button.collidepoint(mouse_pos)
        else GOLD
    )

    py.draw.rect(
        screen, button_colour, button,
        border_radius=6
    )

    draw_text(
        "SELECT LEVEL", button_font, BG,
        button.centerx, button.centery
    )


def level_screen():
    clock = py.time.Clock()
    selected_table = None
    running = True

    while running:
        clock.tick(60)
        mouse_pos = py.mouse.get_pos()

        screen.fill(BG)

        draw_text(
            "SELECT YOUR TABLE", title_font, GOLD,
            WIDTH // 2, 55
        )

        draw_text(
            "Choose your playing ground",
            body_font, WHITE, WIDTH // 2, 110
        )

        draw_card(
            vegas_card,
            vegas_img,
            "LAS VEGAS",
            "The classic casino experience.|"
            "Enter the table and test your poker skills.",
            vegas_button,
            mouse_pos
        )

        draw_card(
            tokyo_card,
            tokyo_img,
            "TOKYO",
            "A modern poker destination inspired by|"
            "the vibrant city of Tokyo.",
            tokyo_button,
            mouse_pos
        )

        back_colour = (
            (35, 100, 70)
            if back_button.collidepoint(mouse_pos)
            else GREEN
        )

        py.draw.rect(screen, back_colour, back_button, border_radius=6)
        draw_text("BACK", button_font, WHITE,
                  back_button.centerx, back_button.centery)

        for event in py.event.get():
            if event.type == py.QUIT:
                return "QUIT"

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    return "BACK"

            if event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if vegas_button.collidepoint(event.pos):
                        selected_table = "Vegas"
                        starting_chips = 70000
                        running = False

                    elif tokyo_button.collidepoint(event.pos):
                        selected_table = "Tokyo"
                        starting_chips = 1000
                        running = False

                    elif back_button.collidepoint(event.pos):
                        return "BACK"

        py.display.flip()

    return selected_table


if __name__ == "__main__":
    result = level_screen()
    print("Selected:", result)
    py.quit()
