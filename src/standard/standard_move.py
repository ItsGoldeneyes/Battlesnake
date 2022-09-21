from standard.minimax_std import Minimax

class StandardMove:
    def __init__(self, board):
        self.board = board

    def choose_move(self, self_snake, depth = 2, debug_mode= False):
        mm = Minimax()
        move = mm.minimax(self.board, self_snake, depth, debug_mode)
        print(move)
        return move[0]
