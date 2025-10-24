import pygame

BOARD_WIDTH = 1000
SIDEBAR_WIDTH = 400
WIDTH = BOARD_WIDTH + SIDEBAR_WIDTH
HEIGHT = BOARD_WIDTH
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_WIDTH//COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

# game modes
HUMAN_VS_AI   = 'Human vs AI'
AI_VS_AI      = 'AI vs AI'
HUMAN_VS_HUMAN = 'Human vs Human'

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
