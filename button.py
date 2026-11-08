import pygame as py


def draw_button(screen, rect, color, text, font, pressed=False):
    py.draw.rect(screen, (35, 35, 35), rect.move(0, 5), border_radius=5)
    if pressed:
        button_rect = rect.move(0, 5)
    else:
        button_rect = rect
    py.draw.rect(screen, color, button_rect, border_radius=5)
    label = font.render(text, True, (255, 255, 255))
    text_rect = label.get_rect(center=button_rect.center)
    screen.blit(label, text_rect)
    
