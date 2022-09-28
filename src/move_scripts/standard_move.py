from algorithms.minimax import Minimax
from move_scripts.standard_move import standard_eval

class StandardMove:
    def __init__(self, board, debug_mode):
        self.debug_mode = debug_mode
        self.board = board

    def choose_move(self, self_snake, depth = 2):
        mm = Minimax()
        move = mm.minimax(self.board, self_snake, depth, self.debug_mode)
        print(move)
        return move[0]
