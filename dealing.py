
import pygame as py
from pathlib import Path
import random
import math


def animate_card(screen, card_image, table_image,
                 start_pos, end_pos, dealt_cards):
    clock = py.time.Clock()
    frames = 30
    start_x, start_y = start_pos
    end_x, end_y = end_pos
    card_width, card_height = card_image.get_size()

    for frame in range(frames + 1):
        t = frame / frames
        progress = t * t * (3 - 2 * t)

        x = start_x + (end_x - start_x) * progress
        y = start_y + (end_y - start_y) * progress

        angle = 720 * (1 - t)
        scale = 0.7 + 0.3 * t

        animated_card = py.transform.rotozoom(card_image, angle, scale)

        screen.blit(table_image, (0, 0))
        for image, position in dealt_cards:
            screen.blit(image, position)

        card_rect = animated_card.get_rect(center=(x, y))
        screen.blit(animated_card, card_rect)

        py.display.flip()
        clock.tick(60)

    final_position = (
        end_x - card_width // 2,
        end_y - card_height // 2
    )

    dealt_cards.append((card_image, final_position))


def deal_cards(screen, table_image, bot_card_back, player_cards):

    dealt_cards = []

    deck_position = (1120, 300)

    animate_card(screen, bot_card_back, table_image,
                 deck_position, (582, 177), dealt_cards)

    animate_card(screen, player_cards[0], table_image,
                 deck_position, (582, 557), dealt_cards)

    animate_card(screen, bot_card_back, table_image,
                 deck_position, (692, 177), dealt_cards)

    animate_card(screen, player_cards[1], table_image,
                 deck_position, (692, 557), dealt_cards)
    return dealt_cards


com_card_images = (
    py.image.load("back1.png").convert_alpha(),
    py.image.load("back2.png").convert_alpha(),
    py.image.load("back2.png").convert_alpha(),
    py.image.load("back1.png").convert_alpha(),
    py.image.load("back1.png").convert_alpha()
)


def load_cards(folder="cards", size=(95, 125)):
    """Load every PNG card image in the cards folder."""

    cards = {}
    card_folder = Path(__file__).parent / "Cards"

    for file_path in card_folder.glob("*.png"):
        image = py.image.load(str(file_path)).convert_alpha()
        image = py.transform.smoothscale(image, size)

        # Filename without extension becomes the dictionary key
        cards[file_path.stem] = image
    print(f"loadded {len(cards)} cards")

    return cards
