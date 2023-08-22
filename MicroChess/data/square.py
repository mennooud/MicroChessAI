# square.py

from const import *

class Square:

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece != None
    
    def isempty(self):
        return not self.has_piece()
    
    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color
    
    def has_rival_piece(self, color):
        return self.has_piece() and self.piece.color != color
        # print(f"Checking rival piece for color {color} at ({self.row}, {self.col}): Has piece? {self.has_piece()}, Piece color: {self.piece.color if self.piece else 'None'}, Result: {result}")
        
    def isempty_or_rival(self, color):
        return self.isempty() or self.has_rival_piece(color)
    
    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg >= ROWS or arg >= COLS:  # updated this line
                return False
        return True