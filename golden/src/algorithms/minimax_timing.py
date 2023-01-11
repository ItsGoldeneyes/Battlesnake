from iteration_utilities import unique_everseen
from multiprocessing import Pool
import copy
import math
import time

class minimax_timing:
    '''
    This function is a Minimax implementation for a game with multiple players.
    The evaluation function as well as gamemode are passed in through the constructor.
    Run Minimax by calling the object
    '''
    def __init__(self, eval_function, gamemode= 'standard', debug_mode=False, alpha_beta=True):
        self.eval_func = eval_function
        self.gamemode = gamemode
        self.debug_mode = debug_mode
        self.alpha_beta = alpha_beta
        self.turn = None
        
    
    def __call__(self, board, depth= 3, snake_id= False):
        self.turn = board.get_turn()
        
        if snake_id:
            minimax_score = self._minimax(snake_id, board, depth)
        else:
            minimax_score = self._minimax(board.get_self_id(), board, depth)
        return minimax_score
    
    
    def dict_next_key(self, dictionary, key):
        '''
        Taken from https://www.geeksforgeeks.org/python-get-next-key-in-dictionary/
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
    
    
    def _minimax(self, snake_id, board, depth, alpha= -math.inf, beta= math.inf):
        if depth == 0:
            return ['leaf', self.eval_func(board, board.get_self_id())]
        
        time_A = time.perf_counter()
        
        # Get snakes early, cleaning  up code
        snakes = board.get_snakes()
        
        # If snake was removed for some reason
        if board.get_self_id() not in snakes:
            return ["snakenotfound", -100]
        
        
        # If snake was removed for some reason
        if snake_id not in snakes:
            return ["snakenotfound", -100]
        
        time_B = time.perf_counter()
        print("snakenotfound took", (time_B-time_A)*1000,'ms')
    

        # Body is doubled up on first turn
        if self.turn == 0:
            board.snakes[snake_id].body.pop()
            snakes = board.get_snakes()
        
        time_A = time.perf_counter()
        
        print("turn 1 check took", (time_A-time_B)*1000,'ms')
        
        # If collision, terminate branch
        if board.collision_check(snakes[board.get_self_id()].get_head(), board.get_self_id()):
            eval = self.eval_func(board, board.get_self_id())
            if eval > 0:
                pass
            return ["collision", eval]
        
        time_B = time.perf_counter()
        print("collision check took", (time_B-time_A)*1000,'ms')
        
        
        potential_moves  = board.get_moves(snakes[snake_id].get_head())
        next_snake_id = self.dict_next_key(snakes, snake_id)
        
        time_A = time.perf_counter()
        print("potential moves took", (time_A-time_B)*1000,'ms')
        
        
        # Apply "wrap fix" to moves, wrapping offscreen moves across the board
        if self.gamemode == 'wrapped':
            temp_moves = {move : board.wrap_fix(potential_moves[move]) for move in potential_moves}
            potential_moves = temp_moves
            
        move_scores = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
        
        time_B = time.perf_counter()
        print("wrap fix took", (time_B-time_A)*1000,'ms')
        
        
        if snake_id == board.get_self_id():
            for move in potential_moves:
                print("MOVE", move)
                time_A = time.perf_counter()
                
                if self.debug_mode:
                    print("\n"+"_____"*depth)
                    print("\n" + "MY_SNAKE", move, "board")
                
                time_B = time.perf_counter()
                print("-- debug mode 1 took", (time_B-time_A)*1000,'ms')
                
                # Copy board and move snake on new board
                move_board = copy.deepcopy(board)
                
                time_A = time.perf_counter()
                print("-- creating move_board took", (time_A-time_B)*1000,'ms')
                
                move_board.move(snake_id, potential_moves[move])
                
                time_B = time.perf_counter()
                print("-- move took", (time_B-time_A)*1000,'ms')
                
                move_board.update_board_after_move() # Make more efficient
                
                time_A = time.perf_counter()
                print("-- update board took", (time_A-time_B)*1000,'ms')
                
                
                if self.debug_mode:
                    move_board.print_board()
                
                time_B = time.perf_counter()
                print("-- debug mode 2 took", (time_B-time_A)*1000,'ms')
                
                move_scores[move] = self._minimax(next_snake_id, move_board, depth-1, alpha, beta)[1]
                
                time_A = time.perf_counter()
                print("-- Recursion took", (time_A-time_B)*1000,'ms')
                
                
                if self.alpha_beta:
                    if move_scores[move] >= beta:
                        break
                    alpha = max(alpha, move_scores[move])
                    
                time_B = time.perf_counter()
                print("-- alpha beta took", (time_B-time_A)*1000,'ms')
                
            if self.debug_mode:
                print(depth, snake_id, move_scores)
                
            best_key = max(move_scores, key=move_scores.get)
            best_move = [best_key, move_scores[best_key]+0.1]
            
            time_A = time.perf_counter()
            print("-- Max key took", (time_A-time_B)*1000,'ms')
            
            return best_move

        else:
            for move in potential_moves:
                if self.debug_mode:
                    print("\n"+"_____"*depth)
                    print("\n" + "OTHER_SNAKE", move, "board")
                
                # Copy board and move snake on new board
                move_board = copy.deepcopy(board)
                move_board.move(snake_id, potential_moves[move])
                move_board.update_board_after_move() # Make more efficient
                if self.debug_mode:
                    move_board.print_board()
                    
                move_scores[move] = self._minimax(next_snake_id, move_board, depth-1, alpha, beta)[1]
                if self.alpha_beta:
                    if move_scores[move] <= alpha:
                        break
                    beta = min(beta, move_scores[move])
                
            if self.debug_mode:
                print(depth, snake_id, move_scores)
                
            best_key = min(move_scores, key=move_scores.get)
            best_move = [best_key, move_scores[best_key]+0.1]

            return best_move