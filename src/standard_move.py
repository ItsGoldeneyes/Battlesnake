from minimax_std import Minimax

class StandardMove:
    def __init__(self, board):
        self.board = board

    def choose_move(self, self_snake, depth = 2):
        mm = Minimax()
        move = mm.minimax(self.board, self_snake, depth)
        print(move)
        return move[0]
