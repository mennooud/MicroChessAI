import copy
from const import ROWS, COLS

def evaluate_board(board):
    total_value = 0
    for row in board.squares:
        for square in row:
            if square.piece:
                total_value += square.piece.value
    return total_value

def generate_all_moves(board, color):
    all_moves = []
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.squares[row][col].piece
            if piece and piece.color == color:
                board.calc_moves(piece, row, col)
                all_moves.extend(piece.moves)
    return all_moves

def minimax(board, depth, is_maximizing, alpha, beta):
    if depth == 0:
        return evaluate_board(board)

    all_moves = generate_all_moves(board, 'white' if is_maximizing else 'black')

    if is_maximizing:
        max_eval = float('-inf')
        for move in all_moves:
            board_copy = copy.deepcopy(board)
            board_copy.move(board_copy.squares[move.initial.row][move.initial.col].piece, move)
            eval = minimax(board_copy, depth-1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in all_moves:
            board_copy = copy.deepcopy(board)
            board_copy.move(board_copy.squares[move.initial.row][move.initial.col].piece, move)
            eval = minimax(board_copy, depth-1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def ai_move(game):
    # print(f"Before move: {game.next_player}'s turn")
    best_move = None
    best_value = float('-inf') if game.next_player == 'white' else float('inf')
    for move in generate_all_moves(game.board, game.next_player):
        board_copy = copy.deepcopy(game.board)
        board_copy.move(board_copy.squares[move.initial.row][move.initial.col].piece, move)
        move_value = minimax(board_copy, 4, game.next_player == 'black', float('-inf'), float('inf'))
        if game.next_player == 'white' and move_value > best_value:
            best_value = move_value
            best_move = move
        elif game.next_player == 'black' and move_value < best_value:
            best_value = move_value
            best_move = move

    if best_move:
        game.board.move(game.board.squares[best_move.initial.row][best_move.initial.col].piece, best_move)
        game.next_turn()