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

            # Show dragged piece above the background
            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # Clicking to select a piece
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.MouseY // SQSIZE
                    clicked_col = dragger.MouseX // SQSIZE

                    # Print position of mouseclick event
                    print('row: ',clicked_row, 'column: ',clicked_col)

                    # clicked on a square if has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece color?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # Show methods
                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)


                # Holding down mousebutton to move a piece
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_background(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)

                # Click release of mouse button to place a piece
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.MouseY // SQSIZE
                        released_col = dragger.MouseX // SQSIZE
                        # Print position of mouseclick event
                        print('row: ',released_row, 'column: ',released_col)

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            # normal capture
                            print('valid move')
                            board.move(dragger.piece, move)

                            
                            # show methods
                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()
                            

                    dragger.undrag_piece()


                # Quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            # Check if the game has ended
            if self.game.end_game():
                break
            
        

main = Main()
main.mainloop()