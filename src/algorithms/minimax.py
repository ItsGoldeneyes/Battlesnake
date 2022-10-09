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
            ik[i] = k     # dictionary key_of_index
        
        # initializing offset
        offset = 1  # (1 for next key, but can be any existing distance)
        
        # Get next key in Dictionary
        index_of_key = ki[key]
        index_of_next_key = (index_of_key + offset) % len(dictionary)
        result = ik[index_of_next_key] if index_of_next_key in ik else None
        
        return result
    
    def _minimax(self, snake_id, board, depth):
        if depth == 0:
            print("LEAF NODE", self.eval_func(board, board.get_self_id()))
            return ['leaf', self.eval_func(board, board.get_self_id())] # Add collision to eval_func
        
        print(snake_id)
        snakes = board.get_snakes()
        potential_moves  = board.find_moves(snakes[snake_id].get_head())
        next_snake_id = self.dict_next_key(snakes, snake_id)
        
        if snake_id == board.get_self_id():
            best_move = ['Error', -math.inf] # Will return if no possible moves
            
            for move in potential_moves:
                    move_board = copy.deepcopy(board)
                    move_board.move(snake_id, potential_moves[move])

                    move_score = self._minimax(next_snake_id, move_board, depth-1)
                    
                    if move_score[1] > best_move[1]:
                        best_move = [move, move_score[1]]
            
            return best_move

        else:
            best_move = ['Error', math.inf] # Will return if no possible moves
            
            for move in potential_moves:
                    move_board = copy.deepcopy(board)
                    move_board.move(snake_id, potential_moves[move])

                    move_score = self._minimax(next_snake_id, move_board, depth-1)
                    
                    if move_score[1] < best_move[1]:
                        best_move = [move, move_score[1]]
            
            return best_move