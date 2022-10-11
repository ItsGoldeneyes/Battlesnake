import copy
import math

from board import Board
from snake import BattleSnake



class minimax:    
    def __init__(self, eval_function, gamemode= 'standard', debug_mode=False):
        self.eval_func = eval_function
        self.gamemode = gamemode
        self.debug_mode = debug_mode
        
    
    def __call__(self, board, depth= 3, snake_id= False):
        if snake_id:
            minimax_score = self._minimax(snake_id, board, depth)
        else:
            minimax_score = self._minimax(board.get_self_id(), board, depth)
        return minimax_score
    
    
    def dict_next_key(self, dictionary, key):
        '''
        Taken from https://www.geeksforgeeks.org/python-get-next-key-in-dictionary/
        O(1)
        '''
        # prepare additional dictionaries
        ki = dict()
        ik = dict()
        for i, k in enumerate(dictionary):
            ki[k] = i   # dictionary index_of_key
            ik[i] = k   # dictionary key_of_index
        
        # initializing offset
        offset = 1  # (1 for next key, but can be any existing distance)
        
        # Get next key in Dictionary
        index_of_key = ki[key]
        index_of_next_key = (index_of_key + offset) % len(dictionary)
        result = ik[index_of_next_key] if index_of_next_key in ik else None
        
        return result
    
    
    def _minimax(self, snake_id, board, depth):
        if depth == 0:
            return ['leaf', self.eval_func(board, board.get_self_id())]
        
        snakes = board.get_snakes()
        
        if snake_id not in snakes:
            return ["collision", -100]
        if board.collision_check(snakes[snake_id].get_head(), snake_id):
            return ["collision", -100]
        
        # print("SNAKE:",snake_id)
        potential_moves  = board.find_moves(snakes[snake_id].get_head())
        next_snake_id = self.dict_next_key(snakes, snake_id)
        
        move_scores = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
        
        for move in potential_moves:
            if self.debug_mode:
                print("\n___________________ ")
                print("\n" + snake_id, move, "board")
                
            move_board = copy.deepcopy(board)
            move_board.move(snake_id, potential_moves[move])
            move_board.update_board_after_move() # Make more efficient
            if self.debug_mode:
                move_board.print_board()
                
            move_scores[move] = self._minimax(next_snake_id, move_board, depth-1)[1]
        if self.debug_mode:
            print(depth, snake_id, move_scores)
        
        if snake_id == board.get_self_id():
            #best_move = ['Error', -math.inf] # Will return if no possible moves
            best_key = max(move_scores, key=move_scores.get)
            best_move = [best_key, move_scores[best_key]]
            
            return best_move

        else:
            #best_move = ['Error', math.inf] # Will return if no possible moves
            best_key = min(move_scores, key=move_scores.get)
            best_move = [best_key, move_scores[best_key]]

            return best_move