import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, HUMAN_VS_AI, AI_VS_AI, HUMAN_VS_HUMAN
from checkers.game import Game
from minimax.algorithm import minimax
from menu.menu import main_menu

FPS = 60
MIN_DEPTH = 1
MAX_DEPTH = 8
DEPTH_STEP = 1

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
    game_window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('DDA Checkers')
    clock = pygame.time.Clock()
    game = Game(game_window)
    depths = (1, 4)

    while True:
        mode = main_menu(game_window, game)

        run = True
        while run:
            clock.tick(FPS)


            # — Always pump events to stay responsive —
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                # Only handle human clicks when needed
                elif event.type == pygame.MOUSEBUTTONDOWN and mode in HUMAN_VS_AI:
                    row, col = get_row_col_from_mouse(event.pos)
                    game.select(row, col)
                    game.update()
                    pygame.time.delay(500)

            # — Then do the moves based on mode —
            if mode == AI_VS_AI:
                white_depth, red_depth = depths
                current_depth = white_depth if game.turn == WHITE else red_depth

                _, new_board = minimax(
                    game.get_board(),
                    current_depth,
                    -float('inf'),
                    float('inf'),
                    True,
                    game,
                    game.turn,
                    game.turn
                )
                game.ai_move(new_board)
                pygame.time.delay(500)

            elif mode == HUMAN_VS_AI and game.turn == WHITE:
                ai_depth = depths[0]
                _, new_board = minimax(
                    game.get_board(),
                    ai_depth,
                    -float('inf'),
                    float('inf'),
                    True,
                    game,
                    WHITE,
                    WHITE
                )
                game.ai_move(new_board)

            # HUMAN_VS_HUMAN just waits on the clicks above

            game.update()

            # after game.update() inside main loop
            winner = game.winner()
            if winner is not None:
                print(f"Winner: {winner}")

                # adjust depths based on Red result:
                # depths is a mutable list [white_depth, red_depth]
                # if RED loses (meaning WHITE won) -> reduce WHITE depth
                # if RED wins -> increase WHITE depth
                if isinstance(depths, tuple):
                    depths = list(depths)  # convert to list so we can modify

                if winner == WHITE:
                    # RED lost -> reduce WHITE depth
                    new_white_depth = max(MIN_DEPTH, depths[0] - DEPTH_STEP)
                    depths[0] = new_white_depth
                    print(f"Adjusting White depth down to {depths[0]}")
                elif winner == RED:
                    # RED won -> increase WHITE depth
                    new_white_depth = min(MAX_DEPTH, depths[0] + DEPTH_STEP)
                    depths[0] = new_white_depth
                    print(f"Adjusting White depth up to {depths[0]}")
                else:  # winner == "Draw" or other draw indicator
                    board = game.get_board()
                    # Prefer board attributes if present
                    white_pieces = getattr(board, "white_left", None)
                    red_pieces = getattr(board, "red_left", None)

                    # Fallback: count pieces by scanning board array
                    if white_pieces is None or red_pieces is None:
                        white_pieces = 0
                        red_pieces = 0
                        for r in board.board:
                            for p in r:
                                if p != 0:
                                    if p.color == WHITE:
                                        white_pieces += 1
                                    else:
                                        red_pieces += 1

                    if white_pieces > red_pieces:
                        depths[0] = max(MIN_DEPTH, depths[0] - DEPTH_STEP)
                        print(
                            f"Draw but White has more pieces ({white_pieces} vs {red_pieces}). Decreasing White depth to {depths[0]}")
                    elif white_pieces < red_pieces:
                        depths[0] = min(MAX_DEPTH, depths[0] + DEPTH_STEP)
                        print(
                            f"Draw but Red has more pieces ({red_pieces} vs {white_pieces}). Increasing White depth to {depths[0]}")
                    else:
                        print(f"Draw and piece count equal ({white_pieces} vs {red_pieces}). No depth change.")

                break

    pygame.quit()

main()