import pygame
import hashlib
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board


class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.state_history = {}  # Track board state repetitions
        self.draw_detected = False  # Flag for draw

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
        self.state_history = {}
        self.draw_detected = False

    def winner(self):
        if self.draw_detected:
            return "Draw"
        return self.board.winner()

    def reset(self):
        self._init()

    def board_state_hash(self):
        # Create a unique string for the board state
        state = []
        for row in self.board.board:
            for piece in row:
                if piece == 0:
                    state.append('0')
                else:
                    state.append(f"{piece.color}-{int(piece.king)}")
        state_str = ','.join(state)
        return hashlib.md5(state_str.encode()).hexdigest()

    def update_state_history(self):
        h = self.board_state_hash()
        self.state_history[h] = self.state_history.get(h, 0) + 1
        # If a state repeats 3 times, declare a draw
        if self.state_history[h] >= 3:
            self.draw_detected = True
            print("Draw: Flip-flopping detected.")
            return True
        return False

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
                self.board.no_capture_moves = 0

                # After a capture, check for further jumps
                self.selected = self.board.get_piece(row, col)
                new_moves = self.board.get_valid_moves(self.selected)
                # Only keep moves that are captures
                capture_moves = {move: skip for move, skip in new_moves.items() if skip}
                if capture_moves:
                    self.valid_moves = capture_moves
                    return True  # Don't change turn, allow another jump
            else:
                self.board.no_capture_moves += 1
                self.selected = None

            self.change_turn()
            self.selected = None

            # Check for flip-flopping draw after each move
            if self.update_state_history():
                # Optionally, handle draw state here (e.g., stop game loop)
                pass
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()
        # Check for flip-flopping draw after each AI move
        if self.update_state_history():
            # Optionally, handle draw state here (e.g., stop game loop)
            pass