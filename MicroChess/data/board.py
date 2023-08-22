# board.py

import copy
import os

from const import *
from square import Square
from piece import *
from move import Move


class Board:

    def __init__(self, game):
        self.game = game
        self.squares = [[0 for col in range(COLS)] for row in range(ROWS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.print_board()

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # Check if a King is captured
        if isinstance(self.squares[final.row][final.col].piece, King):
            winner = 'white' if piece.color == 'black' else 'black'
            self.end_game(winner)

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def in_check(self, piece, move):
        # Simulate the move on the actual board
        initial_piece = self.squares[move.initial.row][move.initial.col].piece
        final_piece = self.squares[move.final.row][move.final.col].piece
        self.squares[move.initial.row][move.initial.col].piece = None
        self.squares[move.final.row][move.final.col].piece = piece

        king_color = piece.color  # We're checking if our own King is in check

        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_rival_piece(king_color):
                    p = self.squares[row][col].piece
                    p.clear_moves()  # Clear existing moves
                    self.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King) and m.final.piece.color == king_color:
                            # Undo the move
                            self.squares[move.initial.row][move.initial.col].piece = initial_piece
                            self.squares[move.final.row][move.final.col].piece = final_piece
                            return True

        # Undo the move
        self.squares[move.initial.row][move.initial.col].piece = initial_piece
        self.squares[move.final.row][move.final.col].piece = final_piece
        return False


    


    def calc_moves(self, piece, row, col, bool=True):
        ''' 
        Calculate all the possible valid moves of a piece on the board.
        ''' 
        def pawn_moves():
            # steps
            steps = 1 if  piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # create a new move
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
                    else: break
                # not in range
                else: break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a new move
                        move = Move(initial, final)
                        
                        # check potencial checks
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
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # Create squares for new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col)
                        # Initiate new move
                        move = Move(initial, final)
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move
                            piece.add_move(move)
                    
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while Square.in_range(possible_move_row, possible_move_col):
                    # create squares of the possible new move
                    initial = Square(row, col)
                    final_piece = self.squares[possible_move_row][possible_move_col].piece
                    final = Square(possible_move_row, possible_move_col, final_piece)
                    # create a possible new move
                    move = Move(initial, final)

                    # empty = continue looping
                    if self.squares[possible_move_row][possible_move_col].isempty():
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)

                    # has enemy piece = add move + break
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

                    # has team piece = break
                    elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                        break

                    # incrementing incrs
                    possible_move_row += row_incr
                    possible_move_col += col_incr

        def king_moves():
            adjs = [
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col) # piece=piece
                        # create new move
                        move = Move(initial, final)
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move
                            piece.add_move(move)

        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1), # down-left
            ])
        
        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0), # up
                (0, 1),  # right
                (1, 0),  # down
                (0, -1)  # left
            ])



        elif isinstance(piece, King):
            adjs = [
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        
                        piece.add_move(move)
        
        

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
        self.squares[4][3] = Square(4, 3, King('white'))
        self.squares[0][0] = Square(0, 0, King('black'))

    def end_game(self, winner):
        self.game.end_game()

    def print_board(self):
        for row in self.squares:
            row_pieces = [square.piece.name if square.piece else 'empty' for square in row]
            print(row_pieces)