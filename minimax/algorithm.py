from copy import deepcopy
import pygame

from checkers import game

RED = (255,0,0)
WHITE = (255, 255, 255)

def minimax(position, depth, alpha, beta, max_player, game, current_color, ai_color):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(ai_color), position

    opponent_color = WHITE if current_color == RED else RED

    print()
    print(max_player)
    if max_player:
        print("maximizing")
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, current_color, game):
            evaluation = minimax(move, depth-1, alpha, beta, False, game, opponent_color, ai_color)[0]
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                print("Alpha beta")
                break
        return maxEval, best_move
    else:
        print("minimizing")
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, current_color, game):
            evaluation = minimax(move, depth-1, alpha, beta, True, game, opponent_color, ai_color)[0]
            if evaluation < minEval:
                minEval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                print("Alpha beta")
                break
        return minEval, best_move

# def minimax(position, depth, alpha, beta, max_player, game, ai_color):
#     if depth == 0 or position.winner() is not None:
#         return position.evaluate(ai_color), position
#
#     print()
#     print (max_player)
#
#     if max_player:
#         maxEval = float('-inf')
#         best_move = None
#         current_color = ai_color
#         print("maximizing")
#         for move in get_all_moves(position, current_color, game):
#             evaluation = minimax(move, depth-1, alpha, beta, False, game, ai_color)[0]
#             if evaluation > maxEval:
#                 maxEval = evaluation
#                 best_move = move
#             alpha = max(alpha, evaluation)
#             if beta <= alpha:
#                 print("Alpha beta")
#                 break
#         return maxEval, best_move
#     else:
#         minEval = float('inf')
#         best_move = None
#         opponent_color = WHITE if ai_color == RED else RED
#         print("minimizing")
#         for move in get_all_moves(position, opponent_color, game):
#             evaluation = minimax(move, depth-1, alpha, beta, True, game, ai_color)[0]
#             if evaluation < minEval:
#                 minEval = evaluation
#                 best_move = move
#             beta = min(beta, evaluation)
#             if beta <= alpha:
#                 print("Alpha beta")
#                 break
#         return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):
    moves = []
    capturing_moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            if skip:
                chain_boards = get_chain_jumps(new_board, temp_piece, game, color)
                if chain_boards:
                    capturing_moves.extend(chain_boards)
                else:
                    capturing_moves.append(new_board)
            else:
                moves.append(new_board)

    # If any capturing moves exist, only return those
    return capturing_moves if capturing_moves else moves

def get_chain_jumps(board, piece, game, color):
    moves = []
    valid_moves = board.get_valid_moves(piece)
    for move, skip in valid_moves.items():
        if skip:
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            further_jumps = get_chain_jumps(new_board, temp_piece, game, color)
            if further_jumps:
                moves.extend(further_jumps)
            else:
                moves.append(new_board)
    return moves