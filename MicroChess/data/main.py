# main.py

import pygame
import sys
import copy
import time

from const import *
from game import Game
from square import Square
from move import Move
from AI import ai_move


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("MicroChess")
        self.game = Game()

    def mainloop(self):

        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
            
        while True:
            # Show methods
            game.show_background(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if game.is_game_over:  # Check if the game is still ongoing
                break

            ai_move(game)            

            pygame.display.update()

            # Check if the game has ended
            if game.is_game_over:
                break

        pygame.quit()



        

main = Main()
main.mainloop()