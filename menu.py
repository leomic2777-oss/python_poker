import pygame as py

screen = None
WIDTH = 1280
HEIGHT = 680
TITLE = None
FONT = None
SMALL = None
home_image = None


def init_menu():
    global TITLE, FONT, SMALL, home_image
    TITLE = py.font.SysFont("Georgia", 42, bold=True)
    FONT = py.font.SysFont("Georgia", 24)
    SMALL = py.font.SysFont("Georgia", 18)
    home_image = py.image.load("homepg.png").convert()


page = "menu"
show_settings = False 
login_name = ""
login_active = False
music_on = False


THEMES = [
    {"name": "Emerald", "felt": (12, 83, 59), "felt_dark": (
        7, 50, 38), "gold": (220, 183, 101)},
    {"name": "Midnight", "felt": (24, 38, 88), "felt_dark": (
        12, 20, 52), "gold": (222, 190, 110)},
    {"name": "Burgundy", "felt": (105, 28, 48), "felt_dark": (
        60, 15, 30), "gold": (230, 190, 116)},
]
theme_index = 0


def centered(screen, text, y, font=FONT, color=(255, 255, 255)):
    surface = font.render(text, True, color)
    screen.blit(surface, surface.get_rect(center=(WIDTH // 2, y)))


def button(screen, rect, label, mouse, active=True, color=None):
    palette = THEMES[theme_index]
    fill = color or palette["gold"]
    hovered = rect.collidepoint(mouse) and active
    draw = tuple(min(255, v + 22) for v in fill) if hovered else fill
    py.draw.rect(screen, draw if active else (
        90, 87, 76), rect, border_radius=10)
    py.draw.rect(screen, (245, 220, 157), rect, 2, border_radius=10)
    text = FONT.render(label, True, (27, 24, 20)
                       if active else (205, 198, 180))
    screen.blit(text, text.get_rect(center=rect.center))
    return hovered


def draw_menu(screen, home_image, rects, mouse):
    if home_image:
        screen.blit(py.transform.smoothscale(
            home_image, (WIDTH, HEIGHT)), (0, 0))
        overlay = py.Surface((WIDTH, HEIGHT), py.SRCALPHA)
        overlay.fill((5, 7, 20, 72))
        screen.blit(overlay, (0, 0))
    else:
        screen.fill((9, 20, 48))
    button(screen, rects["login"], "LOGIN", mouse)
    button(screen, rects["settings"], "SETTINGS", mouse)
    button(screen, rects["exit"], "EXIT", mouse, color=(135, 49, 54))
    if show_settings:
        panel = py.Rect(WIDTH // 2 - 210, HEIGHT // 2 - 112, 420, 224)
        py.draw.rect(screen, (10, 20, 38), panel, border_radius=14)
        py.draw.rect(screen, THEMES[theme_index]
                     ["gold"], panel, 2, border_radius=14)
        centered(screen, "SETTINGS", panel.y + 44,
                 TITLE, THEMES[theme_index]["gold"])
        centered(
            f"Background music: {'ON' if music_on else 'OFF'}  (M)", panel.y + 106, FONT)
        centered(screen, "Press Escape or click outside to close",
                 panel.y + 164, SMALL, (210, 208, 195))
    if page == "themes":
        panel = py.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 78, 500, 156)
        py.draw.rect(screen, (10, 20, 38), panel, border_radius=14)
        py.draw.rect(screen, THEMES[theme_index]
                     ["gold"], panel, 2, border_radius=14)
        centered(screen, "CHOOSE YOUR TABLE", panel.y + 37,
                 FONT, THEMES[theme_index]["gold"])
        centered(screen, "← / → to change   •   Enter to play",
                 panel.y + 100, SMALL)
        centered(screen, THEMES[theme_index]["name"], panel.y + 70, FONT)
    if login_active:
        panel = py.Rect(WIDTH // 2 - 230, HEIGHT // 2 - 80, 460, 160)
        py.draw.rect(screen, (10, 20, 38), panel, border_radius=14)
        py.draw.rect(screen, THEMES[theme_index]
                     ["gold"], panel, 2, border_radius=14)
        centered(screen, "ENTER YOUR NAME", panel.y + 40,
                 FONT, THEMES[theme_index]["gold"])
        centered(screen, login_name + "▏", panel.y + 94, FONT)
