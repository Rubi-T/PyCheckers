import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.no_capture_moves = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def get_all_valid_moves(self, color):
        moves = {}
        for piece in self.get_all_pieces(color):
            piece_moves = self.get_valid_moves(piece)
            if piece_moves:
                moves[piece] = piece_moves
        return moves

    def is_vulnerable(self, piece):
        # Edge pieces are less vulnerable
        if piece.row == 0 or piece.row == ROWS - 1 or piece.col == 0 or piece.col == COLS - 1:
            return False

        # Check if piece is backed up by a friendly piece
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = piece.row + dr, piece.col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                neighbor = self.board[r][c]
                if neighbor != 0 and neighbor.color == piece.color:
                    return False

        # Check if any opponent can capture this piece
        opponent_color = WHITE if piece.color == RED else RED
        for opp_piece in self.get_all_pieces(opponent_color):
            valid_moves = self.get_valid_moves(opp_piece)
            for skipped_pieces in valid_moves.values():
                if piece in skipped_pieces:
                    return True
        return False

    def evaluate(self, ai_color):
        # Weights (tune as needed)
        MATERIAL_W, KING_W = 2.0, 4.0
        ADVANCE_W, CENTER_W = 0.3, 0.3
        EDGE_W, MOBILITY_W = 0.2, 0.3
        CONNECTIVITY_W, VULNERABILITY_W = 0.3, -0.2

        opponent_color = WHITE if ai_color == RED else RED
        score = 0.0

        # Material and kings - compute explicit counts to avoid conditional precedence bugs
        ai_pieces = self.white_left if ai_color == WHITE else self.red_left
        opp_pieces = self.red_left if ai_color == WHITE else self.white_left
        score += MATERIAL_W * (ai_pieces - opp_pieces)

        ai_kings = self.white_kings if ai_color == WHITE else self.red_kings
        opp_kings = self.red_kings if ai_color == WHITE else self.white_kings
        score += KING_W * (ai_kings - opp_kings)

        # Mobility - ensure get_all_valid_moves expects a color and works on this board
        try:
            ai_moves = len(self.get_all_valid_moves(ai_color))
            opp_moves = len(self.get_all_valid_moves(opponent_color))
        except Exception:
            ai_moves = opp_moves = 0
        score += MOBILITY_W * (ai_moves - opp_moves)

        for r in range(ROWS):
            for c in range(COLS):
                piece = self.board[r][c]
                if piece == 0:
                    continue

                piece_is_ai = (piece.color == ai_color)

                # Center control and edge penalties
                if piece.king:
                    if 2 <= r <= 5 and 2 <= c <= 5:
                        score += (CENTER_W if piece_is_ai else -CENTER_W)
                    if r == 0 or r == ROWS - 1 or c == 0 or c == COLS - 1:
                        score += (-EDGE_W if piece_is_ai else EDGE_W)
                else:
                    if 2 <= r <= 5 and 2 <= c <= 5:
                        score += (CENTER_W if piece_is_ai else -CENTER_W)
                    if r == 0 or r == ROWS - 1 or c == 0 or c == COLS - 1:
                        score += (EDGE_W if piece_is_ai else -EDGE_W)

                # Advancement for non-kings
                if not piece.king:
                    advance = r if piece.color == WHITE else (ROWS - 1 - r)
                    score += (advance * ADVANCE_W) if piece_is_ai else (-advance * ADVANCE_W)

                # Connectivity
                adjacents = [(r + dr, c + dc) for dr in (-1, 1) for dc in (-1, 1)
                             if 0 <= r + dr < ROWS and 0 <= c + dc < COLS]
                for ar, ac in adjacents:
                    adj_piece = self.board[ar][ac]
                    if adj_piece != 0 and adj_piece.color == piece.color:
                        score += (CONNECTIVITY_W if piece_is_ai else -CONNECTIVITY_W)

                # Vulnerability - ensure is_vulnerable checks the board 'self' and piece identity on this board
                if self.is_vulnerable(piece):
                    score += (VULNERABILITY_W if piece_is_ai else -VULNERABILITY_W)

        return score

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1 

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves