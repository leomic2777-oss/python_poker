import pygame as py
import menu
import random
from button import draw_button
from chips import draw_chips
from level_select import level_screen
from level_select import draw_text, draw_card
from dealing import animate_card, deal_cards, load_cards
from game import PokerGame
from connector import (
    register_player, get_player_stats,
    record_hand, record_tournament
)

py.init()
py.mixer.init()

screen = py.display.set_mode((1280, 680))
cards = load_cards()

first_card = None
second_card = None

menu.init_menu()
menu.screen = screen
menu.home_image = py.image.load("homepg.png").convert()

menu_rects = {
    "login": py.Rect(490, 470, 300, 55),
    "settings": py.Rect(640, 590, 148, 55),
    "exit": py.Rect(490, 590, 147, 55)
}
        
red_chip_img = py.image.load(
    "vegasredchips.png"
).convert_alpha()

blue_chip_img = py.image.load(
    "vegasbluechips.png"
).convert_alpha()

vtable = py.image.load("vegatable.png").convert()
ttable = py.image.load("tokyotable.png").convert()
ttable = py.transform.scale(ttable, (1280, 680))

current_table = "Vegas"

py.display.set_caption("Definitely Not Gambling")

curr_screen = "Menu"

# LOGIN VARIABLES
username = ""
player_name = ""
login_active = False

login_box = py.Rect(440, 180, 400, 300)
username_box = py.Rect(490, 300, 300, 45)
login_play_button = py.Rect(540, 390, 200, 50)

login_font = py.font.SysFont("georgia", 28, bold=True)
login_input_font = py.font.SysFont("georgia", 24)
login_button_font = py.font.SysFont("georgia", 22, bold=True)

login_active_input = True

# SETTINGS VARIABLES
music_enabled = True

settings_back_button = py.Rect(35, 615, 150, 45)
music_checkbox = py.Rect(530, 300, 35, 35)

settings_font = py.font.SysFont("georgia", 32, bold=True)
settings_text_font = py.font.SysFont("georgia", 25)

running = True
ticksp = py.time.Clock()
font = py.font.Font(None, 29)

call_amount = 0
x, y = 0, 0

py.mixer.music.load("mywaybg.mp3")
py.mixer.music.play(-1)
py.mixer.music.set_volume(0.1)

shuffle_sound = py.mixer.Sound("shuffline.mp3")
allin_sound = py.mixer.Sound("allin.mp3")

music_volume = 0.5
vol_up = py.Rect(1120, 600, 30, 30)
vol_down = py.Rect(1080, 600, 30, 30)

bot_card_back = py.image.load("back1.png").convert_alpha()
bot_card_back = py.transform.scale(bot_card_back, (95, 125))

dealt_cards = []
deal_animation_pending = False

raise_menu_open = False

raise_options = [
    ("0.25x", 0.25),
    ("0.33x", 0.33),
    ("0.5x", 0.50),
    ("0.67x", 0.67),
    ("1x", 1.0),
    ("2x", 2.0),
    ("3x", 3.0),
    ("4x", 4.0),
]

raise_option_rects = [
    py.Rect(
        350 + (i % 3) * 150,
        280 + (i // 3) * 50,
        130, 40
    )
    for i in range(len(raise_options))
]

button_font = py.font.SysFont("georgia", 17, bold=True)

backb = py.Rect(35, 615, 150, 45)
fold_button = py.Rect(400, 440, 110, 30)
check_button = py.Rect(520, 440, 110, 30)
raise_button = py.Rect(640, 440, 110, 30)
allin_button = py.Rect(760, 440, 160, 30)

next_hand_time = None
HAND_DELAY = 2000

game_over_button = py.Rect(490, 390, 300, 55)


# DRAW LOGIN PAGE
def draw_login_page():
    overlay = py.Surface((1280, 680), py.SRCALPHA)
    overlay.fill((0, 0, 0, 190))
    screen.blit(overlay, (0, 0))

    py.draw.rect(
        screen, (23, 74, 53),
        login_box, border_radius=15
    )

    py.draw.rect(
        screen, (214, 182, 110),
        login_box, 3, border_radius=15
    )

    title = login_font.render(
        "PLAYER LOGIN", True, (214, 182, 110)
    )
    screen.blit(
        title,
        title.get_rect(center=(640, 235))
    )

    label = login_input_font.render(
        "Enter Username", True, (255, 255, 255)
    )
    screen.blit(
        label,
        label.get_rect(center=(640, 275))
    )

    py.draw.rect(
        screen, (255, 255, 255),
        username_box, border_radius=6
    )

    username_surface = login_input_font.render(
        username, True, (11, 20, 16)
    )
    screen.blit(
        username_surface,
        (username_box.x + 10, username_box.y + 8)
    )

    button_colour = (
        (35, 100, 70)
        if login_play_button.collidepoint(py.mouse.get_pos())
        else (214, 182, 110)
    )

    py.draw.rect(
        screen, button_colour,
        login_play_button, border_radius=8
    )

    play_text = login_button_font.render(
        "PLAY", True, (11, 20, 16)
    )
    screen.blit(
        play_text,
        play_text.get_rect(center=login_play_button.center)
    )


# REGISTER PLAYER AND OPEN LEVELS
def login_player():
    global username, player_name, login_active, curr_screen

    if username.strip():
        username = username.strip()
        player_name = username

        register_player(player_name)

        print(
            "Player stats:",
            get_player_stats(player_name)
        )

        login_active = False
        curr_screen = "Level"


# DRAW SETTINGS PAGE
def draw_settings_page():
    screen.fill((11, 20, 16))

    title = settings_font.render(
        "SETTINGS", True, (214, 182, 110)
    )
    screen.blit(
        title,
        title.get_rect(center=(640, 150))
    )

    music_text = settings_text_font.render(
        "Background Music", True, (255, 255, 255)
    )
    screen.blit(
        music_text,
        music_text.get_rect(center=(640, 315))
    )

    # Checkbox
    py.draw.rect(
        screen, (255, 255, 255),
        music_checkbox, border_radius=5
    )

    # Tick mark when music is ON
    if music_enabled:
        py.draw.line(
            screen, (23, 74, 53),
            (537, 318), (544, 327), 4
        )
        py.draw.line(
            screen, (23, 74, 53),
            (544, 327), (559, 306), 4
        )

    status = "ON" if music_enabled else "OFF"
    status_text = settings_text_font.render(
        status, True, (214, 182, 110)
    )
    screen.blit(status_text, (585, 365))

    draw_button(
        screen,
        settings_back_button,
        (23, 74, 53),
        "BACK",
        font,
        settings_back_button.collidepoint(py.mouse.get_pos())
    )


while running:
    ticksp.tick(60)

    mouse_pos = py.mouse.get_pos()
    mouse_pressed = py.mouse.get_pressed()[0]

    target = py.Rect((760, 460, 160, 30))
    mpos = py.mouse.get_pos()
    mcoll = target.collidepoint(mpos)

    # MENU SCREEN
    if curr_screen == "Menu":
        menu.draw_menu(
            screen, menu.home_image,
            menu_rects, mouse_pos
        )

    # SETTINGS SCREEN
    elif curr_screen == "Settings":
        draw_settings_page()

    # LEVEL SELECTION SCREEN
    elif curr_screen == "Level":
        selected_table = level_screen()

        if selected_table == "QUIT":
            running = False

        elif selected_table == "BACK":
            curr_screen = "Menu"

        elif selected_table is not None:
            current_table = selected_table

            if current_table == "Vegas":
                player_chips = 70000
                bot_chips = 70000
            else:
                player_chips = 1000
                bot_chips = 1000

            game = PokerGame(
                player_chips=player_chips,
                bot_chips=bot_chips
            )

            tournament_recorded = False
            game.start_hand(list(cards.keys()))

            first_card = cards[game.player_cards[0]]
            second_card = cards[game.player_cards[1]]

            curr_screen = "Game"
            deal_animation_pending = True
            shuffle_sound.play()

    # GAME SCREEN
    elif curr_screen == "Game":

        # Record each completed hand once
        if (
            game.finished
            and game.hand_started
            and not game.hand_recorded
        ):
            record_hand(
                player_name,
                won=(game.winner == "player")
            )
            game.hand_recorded = True

        if game.finished:
            if game.player_chips <= 0 or game.bot_chips <= 0:

                if not tournament_recorded:
                    record_tournament(
                        player_name,
                        won=(
                            game.player_chips > 0
                            and game.bot_chips <= 0
                        )
                    )
                    tournament_recorded = True

                game.stage = "game_over"
                game.winner = (
                    "player"
                    if game.bot_chips <= 0
                    else "bot"
                )
                next_hand_time = None

            else:
                if next_hand_time is None:
                    next_hand_time = (
                        py.time.get_ticks() + HAND_DELAY
                    )

                elif py.time.get_ticks() >= next_hand_time:
                    game.start_hand(list(cards.keys()))

                    if not game.finished:
                        first_card = cards[game.player_cards[0]]
                        second_card = cards[game.player_cards[1]]

                        deal_animation_pending = True
                        shuffle_sound.play()

                    next_hand_time = None
        else:
            next_hand_time = None

        if current_table == "Tokyo":
            screen.blit(ttable, (0, 0))
            table_image = ttable
        else:
            screen.blit(vtable, (0, 0))
            table_image = vtable

        screen.blit(table_image, (0, 0))

        draw_text(
            f"Pot: {game.pot:,}",
            button_font, (255, 255, 255), 640, 400
        )

        draw_text(
            f"Your chips: {game.player_chips:,}",
            button_font, (255, 255, 255), 830, 500
        )

        draw_text(
            game.message,
            button_font, (255, 255, 255), 640, 420
        )

        draw_text(
            f"Bot chips: {game.bot_chips:,}",
            button_font, (255, 255, 255), 830, 220
        )

        back_colour = (
            (35, 100, 70)
            if backb.collidepoint(mouse_pos)
            else (23, 74, 53)
        )

        py.draw.rect(
            screen, back_colour,
            backb, border_radius=6
        )

        draw_text(
            "BACK", button_font, (0, 0, 0),
            backb.centerx, backb.centery
        )

        if deal_animation_pending:
            dealt_cards = deal_cards(
                screen, table_image, bot_card_back,
                [first_card, second_card]
            )
            deal_animation_pending = False

        for image, position in dealt_cards:
            screen.blit(image, position)

        # Reveal bot cards at showdown
        if game.stage in ("showdown", "game_over"):
            bot_card_1 = py.transform.scale(
                cards[game.bot_cards[0]], (95, 125)
            )
            bot_card_2 = py.transform.scale(
                cards[game.bot_cards[1]], (95, 125)
            )

            screen.blit(bot_card_1, (535, 115))
            screen.blit(bot_card_2, (645, 115))

        community_positions = [
            (420, 265), (510, 265), (600, 265),
            (690, 265), (780, 265)
        ]

        for i, position in enumerate(community_positions):
            if i < len(game.community_cards):
                card_image = cards[game.community_cards[i]]
                card_image = py.transform.scale(
                    card_image, (80, 110)
                )
                screen.blit(card_image, position)
            else:
                py.draw.rect(
                    screen, (255, 255, 255),
                    (*position, 80, 110)
                )

        draw_button(
            screen, fold_button, (220, 65, 45),
            "FOLD (F)", font,
            mouse_pressed and fold_button.collidepoint(mouse_pos)
        )

        call_amount = game.amount_to_call()

        button_text = (
            "CALL (C)" if call_amount > 0 else "CHECK (C)"
        )

        draw_button(
            screen, check_button, (45, 180, 75),
            button_text, font,
            mouse_pressed and check_button.collidepoint(mouse_pos)
        )

        draw_button(
            screen, raise_button, (45, 100, 200),
            "RAISE (R)", font,
            mouse_pressed and raise_button.collidepoint(mouse_pos)
        )

        if raise_menu_open and not game.finished:
            for i, (label, multiplier) in enumerate(raise_options):
                rect = raise_option_rects[i]

                py.draw.rect(
                    screen, (35, 45, 65),
                    rect, border_radius=6
                )

                py.draw.rect(
                    screen, (200, 200, 200),
                    rect, 2, border_radius=6
                )

                text_surface = button_font.render(
                    label, True, (255, 255, 255)
                )

                text_rect = text_surface.get_rect(
                    center=rect.center
                )

                screen.blit(text_surface, text_rect)

        draw_button(
            screen, allin_button, (180, 40, 40),
            "ALL IN(SPACE)", font,
            mouse_pressed and allin_button.collidepoint(mouse_pos)
        )

        # Game over popup
        if game.stage == "game_over":
            overlay = py.Surface(
                (1280, 680), py.SRCALPHA
            )
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            if game.winner == "player":
                title = "YOU WIN!"
                title_color = (70, 230, 120)
            else:
                title = "YOU LOSE!"
                title_color = (240, 70, 70)

            title_font = py.font.SysFont(
                "georgia", 58, bold=True
            )

            title_surface = title_font.render(
                title, True, title_color
            )

            screen.blit(
                title_surface,
                title_surface.get_rect(center=(640, 250))
            )

            result_font = py.font.SysFont("georgia", 25)

            result = (
                f"Your chips: {game.player_chips:,}   "
                f"Bot chips: {game.bot_chips:,}"
            )

            result_surface = result_font.render(
                result, True, (255, 255, 255)
            )

            screen.blit(
                result_surface,
                result_surface.get_rect(center=(640, 320))
            )

            draw_button(
                screen, game_over_button, (35, 100, 70),
                "RETURN TO MENU", font,
                game_over_button.collidepoint(mouse_pos)
            )

    # Draw login popup over the current screen
    if login_active:
        draw_login_page()

    # EVENT HANDLING
    for event in py.event.get():

        if event.type == py.QUIT:
            running = False

        # LOGIN EVENTS
        elif login_active:

            if (
                event.type == py.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                if login_play_button.collidepoint(event.pos):
                    login_player()

                elif username_box.collidepoint(event.pos):
                    login_active_input = True

            elif event.type == py.KEYDOWN:
                if event.key == py.K_RETURN:
                    login_player()

                elif event.key == py.K_BACKSPACE:
                    username = username[:-1]

                elif event.unicode.isprintable():
                    if len(username) < 20:
                        username += event.unicode

        # NORMAL MOUSE EVENTS
        elif (
            event.type == py.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            # MENU SCREEN
            if curr_screen == "Menu":

                if menu_rects["login"].collidepoint(event.pos):
                    login_active = True
                    username = ""

                elif menu_rects["settings"].collidepoint(event.pos):
                    curr_screen = "Settings"

                elif menu_rects["exit"].collidepoint(event.pos):
                    running = False

            # SETTINGS SCREEN
            elif curr_screen == "Settings":

                if music_checkbox.collidepoint(event.pos):
                    music_enabled = not music_enabled

                    if music_enabled:
                        py.mixer.music.unpause()
                    else:
                        py.mixer.music.pause()

                elif settings_back_button.collidepoint(event.pos):
                    curr_screen = "Menu"

            # GAME SCREEN
            elif curr_screen == "Game":

                if game.stage == "game_over":
                    if game_over_button.collidepoint(event.pos):
                        curr_screen = "Menu"
                        raise_menu_open = False
                        next_hand_time = None

                elif game.finished:
                    pass

                elif raise_menu_open:
                    for i, rect in enumerate(raise_option_rects):
                        if rect.collidepoint(event.pos):
                            label, multiplier = raise_options[i]

                            game.raise_bet(multiplier)

                            if not game.finished:
                                game.bot_response()

                            break

                    raise_menu_open = False

                else:
                    if backb.collidepoint(event.pos):
                        curr_screen = "Level"
                        next_hand_time = None

                    elif fold_button.collidepoint(event.pos):
                        game.fold()

                    elif check_button.collidepoint(event.pos):
                        game.checkcall()

                        if not game.finished:
                            game.bot_response()

                    elif raise_button.collidepoint(event.pos):
                        raise_menu_open = True

                    elif allin_button.collidepoint(event.pos):
                        game.all_in()
                        allin_sound.play()

                        if not game.finished:
                            game.bot_response()

        # KEYBOARD EVENTS
        elif event.type == py.KEYDOWN:

            if (
                event.key == py.K_ESCAPE
                and curr_screen == "Game"
            ):
                curr_screen = "Level"

            elif curr_screen == "Game":
                if event.key == py.K_SPACE:
                    if not game.finished:
                        game.all_in()
                        allin_sound.play()

    py.display.flip()

py.quit()
