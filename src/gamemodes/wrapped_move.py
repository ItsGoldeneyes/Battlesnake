from algorithms.minimax import Minimax

class WrappedMove:
    '''
    This class handles wrapped BattleSnake turns.
    choose_move is called to kick off a move calculation
    '''
    def __init__(self, board, debug_mode):
        self.debug_mode = debug_mode
        self.board = board

    def choose_move(self, self_snake, depth = 2):
        mm = Minimax(funcs.wrapped_eval, 'wrapped', self.debug_mode)
        move = mm.minimax(self.board, self_snake, depth)
        print(move)
        return move[0]