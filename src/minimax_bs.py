from floodfill_board import floodfill as ff
import random

class Minimax:    
    def minimax(self, board, snake, depth=2):
        eval_state = self.evaluate_state(board, snake)
        potential_moves = board.find_moves(snake.get_head())
        alive_moves = {move : potential_moves[move] for move in potential_moves 
                       if board.collision_check(potential_moves[move])==False}
        best_move = False
        eval_new_state = []
        
        print("start")
        if len(alive_moves) == 0:
            return ["up", -100]
        
        print("move time")
        for move in alive_moves:
            new_board = board.clone()
            snakes = board.get_snakes()
            new_board.move(snake.get_id(), alive_moves[move])
            move_snake = new_board.snakes[snake.get_id()]
            print("move:",move)
            
            # If snake is self, get move evals for other snakes
            if move_snake.get_id() == new_board.get_self_id():
                print("my snake")
                for snake_id in snakes:
                    if snake_id != move_snake.get_id():
                        enemy_snake = new_board.snakes[snake_id]
                        snake_move = self.minimax(new_board, enemy_snake, 0)
                        new_board.move(snake_id, snake_move[0])
                        
            # If deciding for other snakes, prevent infinite loop            
            else:
                print("other snake")
                for snake_id in snakes:
                    new_board.fake_move(snake_id)
            
            # UPDATE BOARD NOT WORKING, doesn't know how to deal with other snakes
            
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
                    
                    
    def evaluate_state(self, board, self_snake):
         # Get moves where snake survives
        potential_moves = board.find_moves(self_snake.get_head())
        alive_moves = {move : potential_moves[move] for move in potential_moves 
                       if board.collision_check(potential_moves[move])==False}
        
        # Set score to a random number between 0 and 1
        score = random.randint(49,51)
        
        move = self_snake.get_head()
        
        # If a collision happens, floodfill
        if len(alive_moves) < 3:
            value_divide = 100
            flooder = ff() # Remove this line when able to do without object
            flood_score = flooder.floodfill(board, move) / value_divide
            score = score + flood_score
            
        # Decrease value if snake not hungry
        if board.get_health(self_snake.id) > 80:
            value_add = -40
            if not board.avoid_food(move):
                score = score + value_add
        
        # Increase value if Snake is hungry
        elif board.get_health(self_snake.id) < 30:
            value_to_subtract_a_multiple = 10
            food_dist = board.food_dist_pos(self_snake.get_head())
            if food_dist == 0:
                food_score = 100
            else:
                food_score = food_dist*-value_to_subtract_a_multiple
            score = score + food_score
            
        return score
     
    
    def evaluate_state_moves(self, self_snake):
        # Get moves where snake survives
        potential_moves = self.board.find_moves(self_snake.get_head())
        alive_moves = {move : potential_moves[move] for move in potential_moves 
                       if self.board.collision_check(potential_moves[move])==False}
        
        # Set scores to a random number between 1 and 5
        scores = {move : random.randint(1,4)*0.25 for move in potential_moves 
                       if self.board.collision_check(potential_moves[move])==False}
        
        # If a collision happens, floodfill
        if len(alive_moves) < 3:
            value_divide = 100
            flooder = ff() # Remove this line when able to do without object
            flood_amt = {move:flooder.floodfill(self.board, alive_moves[move], [])/value_divide 
                         for move in alive_moves}
            if len(set(flood_amt.values())) != 1:
                flood_scores = {}
                pos = 1
                for move in sorted(flood_amt, key=flood_amt.get, reverse=True):
                    flood_scores.update({move: value_divide/pos})
                    pos += 1
                scores = self.add_scores(scores, flood_scores)
            
        # Decrease value if snake not hungry
        if self.board.get_health(self_snake.id) > 90:
            value_add = -10
            no_food_moves = {move : potential_moves[move] for move in potential_moves 
                if self.board.avoid_food(potential_moves[move])==False and 
                    self.board.collision_check(potential_moves[move])==False}
            
            if no_food_moves != {}:
                no_food_scores = {move : value_add for move in alive_moves if move not in no_food_moves}
                scores = self.add_scores(scores, no_food_scores)
        
        # Increase value if Snake is hungry
        elif self.board.get_health(self_snake.id) < 20:
            value_to_divide = 30
            food_dists = self.board.food_dist_moves(self_snake.get_head(), alive_moves)
            if len(set(food_dists.values())) != 1:
                food_scores = {}
                pos = 1
                for move in sorted(food_dists, key=food_dists.get, reverse=False):
                    food_scores.update({move: value_to_divide/pos})
                    pos += 1
                scores = self.add_scores(scores, food_scores)
            
        return scores
                
                
    def add_scores(self, scores, additional_scores):
        new_scores = {}
        for key in scores.keys():
            if key in additional_scores.keys():
                new_scores[key] = scores[key] + additional_scores[key]
            else:
                new_scores[key] = scores[key]
            
        return new_scores