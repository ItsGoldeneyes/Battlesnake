import funcs.evaluate as eval
import funcs.board
import funcs.snake
import random
import time
import math


class BSMinimax():
    def __init__(self, depth=3, ruleset=False) -> None:
        self.eval_func = eval.solo_eval
        # if not ruleset:
        #     self.eval_func = eval.standard_eval
        # elif ruleset == 'solo':
        #     self.eval_func = eval.solo_eval
        # elif ruleset == 'standard':
        #     self.eval_func = eval.standard_eval
        # elif ruleset == 'wrapped':
        #     self.eval_func = eval.wrapped_eval
        
        self.depth = depth
        
    def __call__(self, board) -> dict:
        '''
        Return a the results of single run through minimax.
        '''
        
        self.snake_id = board['snakes'][list(board['snakes'].keys())[0]]['id']
        print(self.snake_id)
        # Get the best move
        move = self._minimax(board, 1, self.snake_id)
        
        return 'left'
    
    def order_moves(self):
        pass
        
    def _minimax(self, board, depth, snake_id=False, alpha=-math.inf, beta=math.inf) -> list:
        '''
        Minimax algorithm, iterate through all snakes before decreasing depth
        '''
        print("Minimax: Depth: {}, Snake: {}".format(depth, snake_id))
        time.sleep(0.5)
        # Base case
        if depth == 0:
            print("base case")
            return ['base', self.eval_func(board, self.snake_id)]
        
        # If not self snake, best move
        if snake_id != self.snake_id:
            print("not self snake")
            time.sleep(0.1)
            best_move = ['up', -math.inf]
            for move in ['up', 'down', 'left', 'right']:
                print('dir: {}'.format(move))
                # Get the board state
                last_state = funcs.board.make_move(board, move, snake_id)
                
                # Get the best move
                eval = -self.eval_func(board, snake_id)
                funcs.board.unmake_move(board, snake_id, last_state)
                if best_move[1] > eval:
                    best_move = [move, eval]
            return best_move
        
        '''
        Not sure if doing this right, supposed to do all snakes at the same time before decreasing depth.
        '''
        
        
        print("is self snake")
        print("recursion time")
        time.sleep(0.5)
        # Run all enemy snakes through, then choose move
        if len(board['snakes']) != 1:
            print("more than one snake")
        
            snake_evals = [[snake['id'], self._minimax(board, depth, snake['id'], alpha, beta)] \
                        for snake in reversed(board['snakes']) \
                        if ['id'] != self.snake_id]
            
            state = funcs.board.get_state(board)
            
            for snake_eval in snake_evals:
                funcs.board.make_move(board, snake_eval[0][0], snake_eval[0][1])
        
        best_move = ['up', -math.inf]
        for move in ['up', 'down', 'left', 'right']:
            move_state = funcs.board.make_move(board, snake_id, move)
            
            move_eval = self._minimax(board, depth-1, snake_id, alpha, beta)
            
            funcs.board.unmake_move(board, snake_id, move_state)
            
            if move_eval > best_move[1]:
                best_move = [move, move_eval]
            
        funcs.board.reset_state(board, state)
        
        return best_move
        
        