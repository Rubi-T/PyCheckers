from copy import deepcopy
import pygame

RED = (255,0,0)
WHITE = (255, 255, 255)

def minimax(position, depth, alpha, beta, max_player, game, ai_color):
    if depth == 0 or position.winner() != None:
        return position.evaluate(ai_color), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        current_color = ai_color
        for move in get_all_moves(position, current_color, game):
            evaluation = minimax(move, depth-1, alpha, beta, False, game, ai_color)[0]
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        opponent_color = WHITE if ai_color == RED else RED
        for move in get_all_moves(position, opponent_color, game):
            evaluation = minimax(move, depth-1, alpha, beta, True, game, ai_color)[0]
            if evaluation < minEval:
                minEval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves
