import pygame
from checkers.constants import AI_VS_AI, HUMAN_VS_AI
from .button import Button

def main_menu(window, game):
    game._init()
    # choose a font and size that mimics your sample (bold uppercase)
    font = pygame.font.SysFont('Arial', 40, bold=True)

    ai_vs_ai_button = Button(text="AI vs AI", pos=(500, 150), font=font)
    player_vs_ai_button = Button(text="Player vs AI", pos=(500, 300), font=font)
    quit_button = Button(text="Quit", pos=(500, 450), font=font, bg_color=(255,255,255), hover_bg=(230,230,230))

    while True:
        window.fill((0,0,0))
        menu_mouse_pos = pygame.mouse.get_pos()

        for b in (ai_vs_ai_button, player_vs_ai_button, quit_button):
            b.changeImageOnHover(menu_mouse_pos)
            b.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ai_vs_ai_button.checkForInput(menu_mouse_pos):
                    return AI_VS_AI
                if player_vs_ai_button.checkForInput(menu_mouse_pos):
                    return HUMAN_VS_AI
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    return None

        pygame.display.update()

def display_sidebar_menu(window):
    # choose a font and size that mimics your sample (bold uppercase)
    font = pygame.font.SysFont('Arial', 40, bold=True)

    help_button = Button(text="Help", pos=(1200, 150), font=font, bg_color=(255,255,255), hover_bg=(230,230,230))
    quit_button = Button(text="Quit", pos=(1200, 450), font=font, bg_color=(255,255,255), hover_bg=(230,230,230))

    menu_mouse_pos = pygame.mouse.get_pos()

    for b in (help_button, quit_button):
        b.changeImageOnHover(menu_mouse_pos)
        b.update(window)

def sidebar_menu_input():
    # choose a font and size that mimics your sample (bold uppercase)
    font = pygame.font.SysFont('Arial', 40, bold=True)

    help_button = Button(text="Help", pos=(1200, 150), font=font, bg_color=(255, 255, 255), hover_bg=(230, 230, 230))
    quit_button = Button(text="Quit", pos=(1200, 450), font=font, bg_color=(255, 255, 255), hover_bg=(230, 230, 230))

    menu_mouse_pos = pygame.mouse.get_pos()
    if help_button.checkForInput(menu_mouse_pos):
        return True
    if quit_button.checkForInput(menu_mouse_pos):
        pygame.quit()
        return None
    return False