import copy
import math
from iteration_utilities import unique_everseen


class Minimax:
    '''
    This function is a Minimax implementation for a game with multiple players.
    The function evaluates for the main snake, then lets the enemy snakes choose their moves.
    After the enemy snakes have chosen their move, the "self snake" chooses the option that maximizes their score.
    This repeats until depth is reached.
    
    The evaluation function as well as gamemode are passed in through the constructor.
    '''
    def __init__(self, eval_func, gamemode= 'standard', debug_mode=False):
        self.eval_func = eval_func
        self.gamemode = gamemode
        self.debug_mode = debug_mode
        
    def minimax(self, board, snake, depth):
        eval_state = self.eval_func(board, snake)
        potential_moves = board.find_moves(snake.get_head())
        alive_moves = {move : potential_moves[move] for move in potential_moves 
                       if board.collision_check(potential_moves[move], snake.get_id(), self.gamemode)==False}
        if self.gamemode == 'wrapped':
            temp_moves = {move : board.wrap_fix(alive_moves[move]) for move in alive_moves}
            alive_moves = temp_moves
        
        eval_new_state = []
        
        is_self = snake.get_id() == board.get_self_id()
        
        # If first turn - body usually doubled up
        if len(snake.body) != len(list(unique_everseen(snake.body))):
            snake.body = list(unique_everseen(snake.body))
            board.snakes[snake.get_id()].body = snake.body
            return self.minimax(board, snake, 0)
        
        if is_self:
            best_move = ["FALSE", -math.inf]
            self_eval = False
            for move in alive_moves:
                if self.debug_mode:
                    print("\n___________________ ")
                    print("\n" + snake.get_id(), move, "board")
                new_board = copy.deepcopy(board)
                snakes = new_board.get_snakes()
                new_board.move(snake.get_id(), alive_moves[move])
                if self.debug_mode:
                    new_board.print_board()
                move_snake = new_board.snakes[snake.get_id()]
                
                # If snake is self, get move evals for other snakes
                for snake_id in snakes:
                    if snake_id != move_snake.get_id():
                        enemy_snake = new_board.snakes[snake_id]
                        snake_move = self.minimax(new_board, enemy_snake, depth= 0)
                        
                        enemy_potential_moves = new_board.find_moves(enemy_snake.get_head())
                        new_board.move(snake_id, enemy_potential_moves[snake_move[0]])
                        # if alive_moves[move] in snake.get_body():
                        #     self_eval = -100

                # if not self_eval:
                #     self_eval = self.eval_func(new_board, move_snake)
                
                # Scoring to be evaluated, is before board update so that food evaluation works
                self_eval = self.eval_func(new_board, move_snake)
                new_board.update_board_after_move()
                
                if self.debug_mode:
                    print(f"Depth: {str(depth)} Score: {str(self_eval)} Snake: {str(move_snake.get_id())}")
                
                # We want to maximize our score
                # If depth is > 0, then minimax. Otherwise, return score
                if depth > 0:
                    eval_new_state = self.minimax(new_board, move_snake, depth-1)
                else:
                    eval_new_state = [move, self_eval]
        
                #If new eval is greater than best move, it becomes new best eval
                if eval_new_state[1] > best_move[1]:
                    best_move = [move, eval_new_state[1]]
                    
        # If enemy snake
        else:
            best_move = ["FALSE", math.inf]
            for move in alive_moves:
                if self.debug_mode:
                    print("\n" + snake.get_id(), move, "board")
                new_board = copy.deepcopy(board)
                snakes = new_board.get_snakes()
                new_board.move(snake.get_id(), alive_moves[move])
                if self.debug_mode:
                    new_board.print_board()
                move_snake = new_board.snakes[snake.get_id()]
                
                # Scoring to be evaluated, is before board update so that food evaluation works
                self_eval = self.eval_func(new_board, move_snake)
                new_board.update_board_after_move()
                
                if self.debug_mode:
                    print(f"Depth: {str(depth)} Score: {str(self_eval)} Snake: {str(move_snake.get_id())}")
                
                # Enemy wants to minimize our score
                # No need for minimax, just evaluate and compare
                eval_new_state = [move, self_eval]
                
                if eval_new_state[1] < best_move[1]:
                    best_move = [move, eval_new_state[1]]
        
        # Best move is list of form [direction, direction_value]
        if best_move[0] == "FALSE":
            print("BEST MOVE FALSE")
            print("ALIVE MOVES:", alive_moves)
            best_move = ["up", -100]
        else:
            best_move[1] = best_move[1] + eval_state
        
        return best_move