import pygame

from checkers.constants import AI_VS_AI, HUMAN_VS_AI
from .button import Button

#constants
AI_VS_AI_IMAGE = pygame.image.load('assets/AIvsAIwhite.png')
AI_VS_AI_IMAGE_HOVER = pygame.image.load('assets/AIvsAIgray.png')
PLAYER_VS_AI_IMAGE = pygame.image.load('assets/PlayervsAIwhite.png')
PLAYER_VS_AI_IMAGE_HOVER = pygame.image.load('assets/PlayervsAIgray.png')

def main_menu(window):
    ai_vs_ai_button = Button(image=AI_VS_AI_IMAGE, hover_image=AI_VS_AI_IMAGE_HOVER, pos=(500, 100))
    player_vs_ai_button = Button(image=PLAYER_VS_AI_IMAGE, hover_image=PLAYER_VS_AI_IMAGE_HOVER, pos=(500, 300))

    while True:
        window.fill((0, 0, 0))  # Fill background with solid black
        menu_mouse_pos = pygame.mouse.get_pos()

        # Update button images based on hover
        ai_vs_ai_button.changeImageOnHover(menu_mouse_pos)
        player_vs_ai_button.changeImageOnHover(menu_mouse_pos)

        ai_vs_ai_button.update(window)
        player_vs_ai_button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ai_vs_ai_button.checkForInput(menu_mouse_pos):
                    return AI_VS_AI
                if player_vs_ai_button.checkForInput(menu_mouse_pos):
                    return HUMAN_VS_AI

        pygame.display.update()