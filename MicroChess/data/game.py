# game.py

import pygame

from const import *
from board import Board
from dragger import Dragger


class Game:
    def __init__(self):
        self.next_player = 'white'
        self.board = Board()
        self.dragger = Dragger()
        self.game_mode = input("Choose game mode\n1: Player vs Player\n2: Player vs Dumb AI\n3: Dumb AI vs Dumb AI\n4: Player vs AI\n5: AI vs AI\n")

    def show_background(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (128, 128, 128)
                else:
                    color = (96, 96, 96)

                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # all pieces except the last one
                    if piece is not self.dragger.piece:
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
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

    def player_vs_player_turn(self):
        '''
        player_vs_player_turn

        Initializes the player versus player game mode.
        '''        
        self.next_player = 'white' if self.next_player == 'black' else 'black'
