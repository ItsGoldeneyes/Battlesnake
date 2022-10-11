from algorithms.minimax import minimax
import gamemodes.wrapped_functions as funcs

class WrappedMove:
    '''
    This class handles wrapped BattleSnake turns.
    choose_move is called to kick off a move calculation
    '''
    def __init__(self, board, debug_mode):
        self.debug_mode = debug_mode
        self.board = board

    def choose_move(self, depth = 2):
        
        mm = minimax(eval_function= funcs.wrapped_eval,
                           debug_mode= self.debug_mode)
        mm_score = mm(self.board, depth)
        
        print(mm_score)
        return mm_score[0]