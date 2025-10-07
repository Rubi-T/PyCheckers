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
        MATERIAL_W, KING_W = 2.0, 3.5
        ADVANCE_W, CENTER_W = 0.2, 0.2
        EDGE_W, MOBILITY_W = 0.1, 0.2
        CONNECTIVITY_W, VULNERABILITY_W = 0.2, -0.3

        opponent_color = WHITE if ai_color == RED else RED
        score = 0

        # Material and kings
        score += MATERIAL_W * (self.white_left if ai_color == WHITE else self.red_left
                                                                         - self.red_left if ai_color == WHITE else self.white_left)
        score += KING_W * (self.white_kings if ai_color == WHITE else self.red_kings
                                                                      - self.red_kings if ai_color == WHITE else self.white_kings)

        # Mobility
        score += MOBILITY_W * (len(self.get_all_valid_moves(ai_color)) - len(self.get_all_valid_moves(opponent_color)))

        for r in range(ROWS):
            for c in range(COLS):
                piece = self.board[r][c]
                if piece != 0:
                    # Center control
                    if piece.king:
                        # Strong center bonus for kings
                        if 2 <= r <= 5 and 2 <= c <= 5:
                            if piece.color == ai_color:
                                score += 1.0
                            else:
                                score -= 1.0
                        # Strong edge penalty for kings
                        if r == 0 or r == ROWS - 1 or c == 0 or c == COLS - 1:
                            if piece.color == ai_color:
                                score -= 1.0
                            else:
                                score += 1.0
                    else:
                        # Center control for non-kings
                        if 2 <= r <= 5 and 2 <= c <= 5:
                            if piece.color == ai_color:
                                score += CENTER_W
                            else:
                                score -= CENTER_W
                        # Edge safety for non-kings
                        if r == 0 or r == ROWS - 1 or c == 0 or c == COLS - 1:
                            if piece.color == ai_color:
                                score += EDGE_W
                            else:
                                score -= EDGE_W
                    # Advancement for non-kings
                    if not piece.king:
                        advance = r if piece.color == WHITE else (ROWS - 1 - r)
                        if piece.color == ai_color:
                            score += advance * ADVANCE_W
                        else:
                            score -= advance * ADVANCE_W
                    # Connectivity (adjacent friendly pieces)
                    adjacents = [(r + dr, c + dc) for dr in [-1, 1] for dc in [-1, 1]
                                 if 0 <= r + dr < ROWS and 0 <= c + dc < COLS]
                    for ar, ac in adjacents:
                        adj_piece = self.board[ar][ac]
                        if adj_piece != 0 and adj_piece.color == piece.color:
                            if piece.color == ai_color:
                                score += CONNECTIVITY_W
                            else:
                                score -= CONNECTIVITY_W
                    # Vulnerability (can be captured next turn)
                    # This requires a helper to check if piece is capturable
                    if self.is_vulnerable(piece):
                        if piece.color == ai_color:
                            score += VULNERABILITY_W
                        else:
                            score -= VULNERABILITY_W

        return score

    # def evaluate(self, ai_color):
    #     # weights
    #     MATERIAL_W, KING_W = 1.0, 1.5
    #     KING_CENTER_W, KING_EDGE_P = 1.5, -1.5
    #     ADVANCE_W = 0.2
    #     MOVE_PENALTY = 0.5
    #
    #     # Determine opponent color
    #     opponent_color = WHITE if ai_color == RED else RED
    #
    #     # 1) Material & Kings
    #     ai_material = self.white_left if ai_color == WHITE else self.red_left
    #     opp_material = self.red_left if ai_color == WHITE else self.white_left
    #
    #     ai_kings = self.white_kings if ai_color == WHITE else self.red_kings
    #     opp_kings = self.red_kings if ai_color == WHITE else self.white_kings
    #
    #     score = MATERIAL_W * (ai_material - opp_material)
    #     score += KING_W * (ai_kings - opp_kings)
    #
    #     # 2) Positional bonuses/penalties
    #     for r in range(ROWS):
    #         for c in range(COLS):
    #             piece = self.board[r][c]
    #             if piece != 0:
    #                 if piece.king:
    #                     if piece.color == ai_color:
    #                         # Center bonus
    #                         if 2 <= r <= 5 and 2 <= c <= 5:
    #                             score += KING_CENTER_W
    #                         # Edge penalty: any edge, not just corners
    #                         if r == 0 or r == ROWS - 1 or c == 0 or c == COLS - 1:
    #                             score += KING_EDGE_P
    #                     elif piece.color == opponent_color:
    #                         if 2 <= r <= 5 and 2 <= c <= 5:
    #                             score -= KING_CENTER_W
    #                         if r == 0 or r == ROWS - 1 or c == 0 or c == COLS - 1:
    #                             score -= KING_EDGE_P
    #                 else:
    #                     # Non-king positional scoring: reward advancing
    #                     if piece.color == ai_color:
    #                         advance = r if ai_color == WHITE else (ROWS - 1 - r)
    #                         score += advance * ADVANCE_W
    #                     else:
    #                         advance = r if piece.color == WHITE else (ROWS - 1 - r)
    #                         score -= advance * ADVANCE_W
    #
    #     # 3) Tempo penalty for non-capture moves
    #     score -= MOVE_PENALTY * self.no_capture_moves
    #
    #     return score

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