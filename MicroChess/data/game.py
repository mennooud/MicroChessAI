# game.py

import pygame

from const import *
from board import Board
from dragger import Dragger
from square import Square
from piece import King

class Game:

    def __init__(self):
        self.next_player = 'white'
        # self.board  = Board()
        self.dragger = Dragger()
        self.turn_count = 0
        self.board  = Board(self)

    # Blit methods

    def show_background(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (128, 128, 128)
                else:
                    color = (96, 96, 96)

                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rect)

    # Other methods

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                        piece = self.board.squares[row][col].piece
                        # Image texture
                        img = pygame.image.load(piece.texture)

                        # Rect
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        
                        # Blit
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                # color
                color = (200, 100, 100) if (move.final.row + move.final.col) % 2 == 0 else (200, 70, 70)
                # rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = (200, 100, 100) if (pos.row + pos.col) % 2 == 0 else (200, 70, 70)
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)


    # Other methods
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
        self.turn_count += 1

    def end_game(self):
        white_king_present = False
        black_king_present = False

        for row in self.board.squares:
            for square in row:
                if square.piece:
                    if isinstance(square.piece, King):
                        if square.piece.color == 'white':
                            white_king_present = True
                        elif square.piece.color == 'black':
                            black_king_present = True

        if not white_king_present:
            print("White king missing!")
            winner = 'black'
        elif not black_king_present:
            print("Black king missing!")
            winner = 'white'
        else:
            return False  # No king has been captured, so the game hasn't ended

        print(f"{winner} wins in {self.turn_count} turns!")
        pygame.quit()
        return True

