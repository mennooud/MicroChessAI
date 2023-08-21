# main.py

import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('MicroChess')
        self.game = Game()

    def mainloop(self):

        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        game_mode = game.game_mode

        while True:
            game.show_background(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                # clicking on the pieces
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    
                    clicked_row = dragger.MouseY // SQSIZE
                    clicked_col = dragger.MouseX // SQSIZE

                    # clicked on a square if has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid color piece?
                        if piece.color == game.next_player:

                            board.calc_moves(piece, clicked_row, clicked_col, bool=True) # noqa
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods
                            game.show_background(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # mousemotion of the pieces
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_background(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)
                
                # click release of the pieces
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        
                        released_row = dragger.MouseY // SQSIZE
                        returned_col = dragger.MouseX // SQSIZE


                        print(f"Released row: {released_row}, Released column: {returned_col}")  # Print the released row and column

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, returned_col)
                        move = Move(initial, final) 
                        # check if move is valid
                        is_valid_move = board.valid_move(dragger.piece, move)
                        print(f"Is valid move: {is_valid_move}")  # Print whether the move is valid
                        
                        if board.valid_move(dragger.piece, move):
                            # normal move
                            board.move(dragger.piece, move)

                            # show methods
                            game.show_background(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                            # # next turn
                            # if game_mode == '1':
                            #     # switch turn to the next player
                            #     game.next_player = 'black' if game.next_player == 'white' else 'white'
                            # elif game_mode == '2':
                            #     game.player_vs_dumb_ai_turn()
                            # elif game_mode == '4':
                            #     game.player_vs_smarter_ai_turn()
                            # elif game_mode == '5':
                            #     game.ai_vs_ai_turn()

                            # check for checkmate
                            if board.in_check(dragger.piece, move, print_message=True):
                                if board.checkmate(dragger.piece.color):
                                    print(f'{dragger.piece.color} is in checkmate.')
                                    pygame.quit()
                                    sys.exit()

                            game.next_player = 'black' if game.next_player == 'white' else 'white'

                    dragger.undrag_piece()

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

main = Main()
main.mainloop()