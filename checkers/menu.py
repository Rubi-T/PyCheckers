import pygame
from checkers.constants import AI_VS_AI, HUMAN_VS_AI
from .button import Button

def main_menu(window, game, depths):
    game._init()
    # choose a font and size that mimics your sample (bold uppercase)
    font = pygame.font.SysFont('Arial', 40, bold=True)

    ai_vs_ai_button = Button(text="AI vs AI", pos=(700, 150), font=font)
    player_vs_ai_button = Button(text="Player vs AI", pos=(700, 300), font=font)
    quit_button = Button(text="Quit", pos=(700, 450), font=font, bg_color=(255,255,255), hover_bg=(230,230,230))
    custom_depths_button = Button(text="Set Depths", pos=(700, 600), font=font, bg_color=(255, 255, 255), hover_bg=(230, 230, 230))

    while True:
        window.fill((0,0,0))
        menu_mouse_pos = pygame.mouse.get_pos()

        for b in (ai_vs_ai_button, player_vs_ai_button, quit_button, custom_depths_button):
            b.changeImageOnHover(menu_mouse_pos)
            b.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ai_vs_ai_button.checkForInput(menu_mouse_pos):
                    return AI_VS_AI, depths
                if player_vs_ai_button.checkForInput(menu_mouse_pos):
                    return HUMAN_VS_AI, depths
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    return None
                if custom_depths_button.checkForInput(menu_mouse_pos):
                    input_active = True
                    input_box1 = pygame.Rect(700, 200, 140, 50)
                    input_box2 = pygame.Rect(700, 300, 140, 50)
                    color_inactive = pygame.Color('lightskyblue3')
                    color_active = pygame.Color('dodgerblue2')
                    color1 = color_inactive
                    color2 = color_inactive
                    text1 = ''
                    text2 = ''
                    active1 = False
                    active2 = False
                    font_input = pygame.font.Font(None, 40)

                    while input_active:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                return None
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                active1 = input_box1.collidepoint(event.pos)
                                active2 = input_box2.collidepoint(event.pos)
                                color1 = color_active if active1 else color_inactive
                                color2 = color_active if active2 else color_inactive
                            if event.type == pygame.KEYDOWN:
                                if active1:
                                    if event.key == pygame.K_RETURN:
                                        active1 = False
                                    elif event.key == pygame.K_BACKSPACE:
                                        text1 = text1[:-1]
                                    else:
                                        text1 += event.unicode
                                elif active2:
                                    if event.key == pygame.K_RETURN:
                                        active2 = False
                                    elif event.key == pygame.K_BACKSPACE:
                                        text2 = text2[:-1]
                                    else:
                                        text2 += event.unicode
                                if event.key == pygame.K_RETURN and text1 and text2:
                                    try:
                                        depths = [int(text1), int(text2)]
                                        print("Depths set to:", depths)
                                        input_active = False
                                    except ValueError:
                                        print("Please enter valid integers.")

                        window.fill((30, 30, 30))
                        pygame.draw.rect(window, color1, input_box1)
                        pygame.draw.rect(window, color2, input_box2)

                        txt_surface1 = font_input.render(text1, True, (255, 255, 255))
                        txt_surface2 = font_input.render(text2, True, (255, 255, 255))
                        window.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 5))
                        window.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 5))

                        pygame.display.flip()

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