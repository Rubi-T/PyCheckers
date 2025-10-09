import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, HUMAN_VS_AI, AI_VS_AI, HUMAN_VS_HUMAN
from checkers.game import Game
from minimax.algorithm import minimax
from menu.menu import main_menu

FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('DDA Checkers')

def setup_mode_and_depths():
    # 1. Let user pick game mode
    modes = [HUMAN_VS_AI, AI_VS_AI, HUMAN_VS_HUMAN]
    print("Select game mode:")
    for i, m in enumerate(modes, start=1):
        print(f"{i}. {m}")
    choice = int(input("Enter 1, 2 or 3: ").strip())
    mode = modes[choice - 1]

    # 2. Based on mode, ask for depths
    if mode == AI_VS_AI:
        white_depth = int(input("White AI depth (e.g. 2–6): ").strip())
        red_depth   = int(input("Red AI depth   (e.g. 2–6): ").strip())
        depths = (white_depth, red_depth)
    elif mode == HUMAN_VS_AI:
        ai_depth = int(input("AI depth (e.g. 2–6): ").strip())
        depths = (ai_depth,)
    else:
        depths = ()  # Human vs Human needs no depth

    return mode, depths


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game(window)
    depths = (6, 1)
    mode = main_menu(window)

    run = True
    while run:
        clock.tick(60)

        # — Always pump events to stay responsive —
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Only handle human clicks when needed
            elif event.type == pygame.MOUSEBUTTONDOWN and mode in (HUMAN_VS_AI, HUMAN_VS_HUMAN):
                row, col = get_row_col_from_mouse(event.pos)
                game.select(row, col)

        # — Then do the moves based on mode —
        if mode == AI_VS_AI:
            white_depth, red_depth = depths
            current_depth = white_depth if game.turn == WHITE else red_depth
            is_max        = (game.turn == WHITE)

            _, new_board = minimax(
                game.get_board(),
                current_depth,
                -float('inf'),
                float('inf'),
                is_max,
                game,
                WHITE
            )
            game.ai_move(new_board)
            pygame.time.delay(200)

        elif mode == HUMAN_VS_AI and game.turn == RED:
            ai_depth = depths[0]
            _, new_board = minimax(
                game.get_board(),
                ai_depth,
                -float('inf'),
                float('inf'),
                False,
                game,
                RED
            )
            game.ai_move(new_board)

        # HUMAN_VS_HUMAN just waits on the clicks above

        game.update()

        if game.winner() is not None:
            print(f"Winner: {game.winner()}")
            run = False

    pygame.quit()

# def main():
#     run = True
#     clock = pygame.time.Clock()
#     game = Game(WIN)
#
#     while run:
#

    #     clock.tick(FPS)
    #
    #     if game.turn == WHITE:
    #         value, new_board = minimax(game.get_board(), 1, float('-inf'), float('inf'), WHITE, game)
    #         game.ai_move(new_board)
    #
    #     if game.winner() != None:
    #         print(game.winner())
    #         run = False
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             run = False
    #
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             pos = pygame.mouse.get_pos()
    #             row, col = get_row_col_from_mouse(pos)
    #             game.select(row, col)
    #
    #     game.update()
    #
    # pygame.quit()

main()