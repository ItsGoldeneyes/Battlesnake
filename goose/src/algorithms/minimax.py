import funcs.evaluate as eval
import funcs.board
import funcs.snake
import random
import math


class BSMinimax():
    def __init__(self, depth=3, ruleset=False) -> None:
        if not ruleset:
            self.eval_func = eval.standard_eval()
        elif ruleset == 'solo':
            self.eval_func = eval.solo_eval()
        elif ruleset == 'standard':
            self.eval_func = eval.standard_eval()
        elif ruleset == 'wrapped':
            self.eval_func = eval.wrapped_eval()
        
        self.depth = depth
        
    def __call__(self) -> dict:
        '''
        Return the results of single run through minimax.
        '''
        return 'right'
    
    def order_moves(self):
        pass
        
    def _minimax(self, board, snake_id, depth, alpha=-math.inf, beta=math.inf, maximizing_player = True) -> int:
        '''
        Minimax algorithm, collect all snake's moves by iterating through snakes
        '''
        pass