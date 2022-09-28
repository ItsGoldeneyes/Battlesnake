import move_scripts.wrapped_functions as funcs
from algorithms.minimax import Minimax

class WrappedMove:
    def __init__(self, board):
        self.board = board

    def choose_move(self, self_snake, depth = 2):
        mm = Minimax(funcs.wrapped_eval)
        move = mm.minimax(self.board, self_snake, depth)
        print(move)
        return move[0]
