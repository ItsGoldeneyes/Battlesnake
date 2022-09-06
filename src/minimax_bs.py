from floodfill_board import floodfill as ff
import random

class Minimax:    
    def minimax(self, board, snake, depth=2):
        eval_state = self.evaluate_state(board, snake)
        potential_moves = board.find_moves(snake.get_head())
        alive_moves = {move : potential_moves[move] for move in potential_moves 
                       if board.collision_check(potential_moves[move], snake.get_id())==False}
        best_move = False
        eval_new_state = []
        
        # print("start")
        if len(alive_moves) == 0:
            return ["up", -100]
        
        # print("move time")
        for move in alive_moves:
            new_board = board.clone()
            snakes = board.get_snakes()
            new_board.move(snake.get_id(), alive_moves[move])
            move_snake = new_board.snakes[snake.get_id()]
            # print("move:", move)
            
            # If snake is self, get move evals for other snakes
            if move_snake.get_id() == new_board.get_self_id():
                # print("my snake")
                for snake_id in snakes:
                    if snake_id != move_snake.get_id():
                        enemy_snake = new_board.snakes[snake_id]
                        snake_move = self.minimax(new_board, enemy_snake, 0)
                        new_board.move(snake_id, snake_move[0])
                        
            # If deciding for other snakes, prevent infinite loop            
            else:
                # print("other snake")
                for snake_id in snakes:
                    new_board.fake_move(snake_id)
            
            # print('update_board')
            # print(new_snake.get_board().snakes)
            # new_board.update_board_after_move()
            # new_snake.board_update(new_board)
            
            
            if depth > 0:
                eval_new_state = self.minimax(new_board, move_snake, depth-1)
            else:
                eval_new_state = [move, self.evaluate_state(new_board, move_snake)]
            
            if best_move:
                if eval_new_state[1] > best_move[1]:
                    best_move = [move, eval_new_state[1]]
            else:
                best_move = [move, eval_new_state[1]]
            
        best_move[1] = best_move[1] + eval_state
        
        return best_move
                    
                    
    def evaluate_state(self, board, snake): # Scoring not working correctly
         # Get moves where snake survives
        potential_moves = board.find_moves(snake.get_head())
        alive_moves = {move : potential_moves[move] for move in potential_moves 
                       if board.collision_check(potential_moves[move], snake.get_id())==False}
        
        # Set score to a random number between 49 and 51
        score = random.randint(49,51)
        move = snake.get_head()
        
        # If a collision is possible, floodfill
        if len(alive_moves) <= 2:
            flooder = ff() # Remove this line when able to do without object
            flood_score = flooder.floodfill_bucket(board, flooder.floodfill(board, move, snake.get_id()))
            # print("FLOODFILL:", flood_score)
            score = score + flood_score
            
        # Decrease food value if snake not hungry
        # if board.get_health(snake.id) > 80:
        #     value_add = -40
        #     if not board.avoid_food(move):
        #         score = score + value_add
        
        # Increase food relative value if snake is hungry
        if board.get_health(snake.id) < 30 or board.relative_length(snake.id) > 0:
            # print("HUNGRY")
            value_add = -10
            food_dist = board.food_dist_pos(snake.get_head())
            food_score = food_dist*value_add
            score = score + food_score
            
        return score