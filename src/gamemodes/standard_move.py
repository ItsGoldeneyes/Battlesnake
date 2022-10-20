import gamemodes.standard_functions as funcs
from algorithms.minimax import minimax
import random

class StandardMove:
    '''
    This class handles standard BattleSnake turns.
    choose_move is called to kick off a move calculation
    '''
    def __init__(self, board, debug_mode):
        self.debug_mode = debug_mode
        self.board = board

    def choose_move(self, depth = 2):
        
        mm = minimax(eval_function= funcs.standard_eval,
                           debug_mode= self.debug_mode)
        mm_score = mm(self.board, depth)
        
        # If given move is a collision, choose random alive move
        if mm_score[1] < 0:
            possible_moves = self.board.get_moves(self.board.snakes[self.board.get_self_id()].get_head())
            alive_moves = [move for move in possible_moves if not self.board.collision_check(possible_moves[move])]
            if len(alive_moves) == 0:
                pass
            else:
                return random.choice(alive_moves)
        
        return mm_score
