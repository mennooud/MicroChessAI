# board.py

import copy

from const import *
from square import Square
from piece import *
from move import Move

class Board:

    def __init__(self):
        self.squares = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = 'white'
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move, testing=False):
        initial_piece = self.squares[move.initial.row][move.initial.col].piece
        final_piece = self.squares[move.final.row][move.final.col].piece

        # Check if the move is valid
        if self.valid_move(piece, move):

            # Move piece
            self.squares[move.final.row][move.final.col].piece = piece
            self.squares[move.initial.row][move.initial.col].piece = None

            # Set moved attribute
            if piece is not None:
                piece.moved = True

            # Update moves for the piece
            piece.clear_moves()
            if piece.name == 'pawn':
                self.pawn_moves()
            elif piece.name == 'knight':
                self.knight_moves()
            elif piece.name == 'bishop':
                self.diagonal_moves()
            elif piece.name == 'rook':
                self.straightline_moves()
            elif piece.name == 'queen':
                self.diagonal_moves()
                self.straightline_moves()
            elif piece.name == 'king':
                self.king_moves()

            # Check if the move puts the player in check
            if not testing and self.in_check(piece, move, print_message=False):
                self.move(initial_piece, Move(move.final, move.initial), testing=True)  # Undo the move
                return False

            return True

        return False

    def valid_move(self, piece, move):
        if not Square.in_range(move.initial.row, move.initial.col, move.final.row, move.final.col):
            return False  # Move is out of range

        initial_piece = self.squares[move.initial.row][move.initial.col].piece
        dest_piece = self.squares[move.final.row][move.final.col].piece

        if not initial_piece or (dest_piece and dest_piece.color == initial_piece.color):
            return False  # Invalid move

        valid_moves = [m for m in initial_piece.moves if m.initial.row == move.initial.row and m.initial.col == move.initial.col]
        if not any(m.final.row == move.final.row and m.final.col == move.final.col for m in valid_moves):
            return False  # Move is not in piece's moves

        # Add more rules for other pieces if needed

        return True

    def in_check(self, piece, move, print_message=False):
        temp_game = copy.deepcopy(self)
        temp_piece = temp_game.squares[move.initial.row][move.initial.col].piece
        temp_game.move(temp_piece, move, testing=True)
        
        rival_color = 'white' if piece.color == 'black' else 'black'
        rival_king = None
        
        # Find the rival king
        for row in range(ROWS):
            for col in range(COLS):
                if temp_game.squares[row][col].has_piece():
                    rival_piece = temp_game.squares[row][col].piece
                    if isinstance(rival_piece, King) and rival_piece.color == rival_color:
                        rival_king = temp_game.squares[row][col]  # Store the square, not the piece
                        break
            if rival_king:
                break
        
        if not rival_king:
            return False  # Rival king not found, not in check
        
        # Calculate moves for pieces of the rival color
        for row in range(ROWS):
            for col in range(COLS):
                if temp_game.squares[row][col].has_piece() and temp_game.squares[row][col].piece.color == rival_color:
                    rival_piece = temp_game.squares[row][col].piece
                    temp_game.calc_moves(rival_piece, row, col, bool=False)
                    for rival_move in rival_piece.moves:
                        if rival_move.final == rival_king:
                            if print_message:
                                print(f'{rival_piece.color} is in check')
                            return True
        
        return False
    
    def checkmate(self, color):
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_team_piece(color):
                    piece = self.squares[row][col].piece
                    self.calc_moves(piece, row, col, bool=True)
                    if piece.moves:
                        return False
        return True

    def calc_moves(self, piece, row, col, bool=True):
        '''
        Calculates all possible moves for a piece.
        '''
        def pawn_moves():
            # steps of pawn movement
            if piece.moved:
                steps = 1
            else:
                steps = 2

            # vertical movement
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create initial and final moves
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)

                        # create new move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)
                    # blocked
                    else:
                        break
                # not in range
                else:
                    break

            # diagonal movement
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color): # noqa
                        # create initial and final moves
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece # noqa
                        final = Square(possible_move_row, possible_move_col, final_piece) # noqa
                        # create new move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)          

        def knight_moves():
            possible_moves = [
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row + 1, col + 2),
                (row + 1, col - 2),
                (row - 1, col + 2),
                (row - 1, col - 2)
            ]
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color): # noqa
                        # create squares of the new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece # noqa
                        final = Square(possible_move_row, possible_move_col, final_piece) # noqa
                        # create a new move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        # create squares of the new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece # noqa
                        final = Square(possible_move_row, possible_move_col, final_piece) # noqa
                        # create a new move
                        move = Move(initial, final)
                        
                        # empty squares of the new move
                        if self.squares[possible_move_row][possible_move_col].isempty(): # noqa
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

                        # has rival piece
                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
                            break

                        # has team piece
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    # not in range
                    else:
                        break

                    # incrementing the row and col
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row - 1, col - 0),
                (row - 1, col + 1),
                (row + 0, col + 1),
                (row + 1, col + 1),
                (row + 1, col + 0),
                (row + 1, col - 1),
                (row + 0, col - 1),
                (row - 1, col - 1)
            ]
            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color): # noqa
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create a new move
                        move = Move(initial, final)
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)

               
        if piece.name == 'pawn':
            pawn_moves()

        elif piece.name == 'knight':
            knight_moves()

        elif piece.name == 'bishop':
            straightline_moves([
                (1, 1),
                (-1, 1),
                (1, -1),
                (-1, -1)
            ])   

        elif piece.name == 'rook':
            straightline_moves([
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1)
            ]) 

        elif piece.name == 'king':
            king_moves()

        print(f"Calculated moves for piece at row {row}, column {col}: {piece.moves}")

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        # Pawns
        self.squares[3][0] = Square(2, 0, Pawn('white'))
        self.squares[1][3] = Square(0, 3, Pawn('black'))

        # Knights
        self.squares[4][2] = Square(2, 0, Knight('white'))
        self.squares[0][1] = Square(0, 3, Knight('black'))
      
        # Bishops
        self.squares[4][1] = Square(4, 1, Bishop('white'))
        self.squares[0][2] = Square(0, 2, Bishop('black'))

        # Rooks
        self.squares[4][0] = Square(4, 0, Rook('white'))
        self.squares[0][3] = Square(0, 3, Rook('black'))

        # King
        self.squares[4][3] = Square(4, 0, King('white'))
        self.squares[0][0] = Square(0, 0, King('black'))