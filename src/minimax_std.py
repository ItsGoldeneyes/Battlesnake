import copy
from iteration_utilities import unique_everseen


class Minimax:    
    def minimax(self, board, snake, depth, print_output= False):
        # eval_state = self.evaluate_state(board, snake)
        potential_moves = board.find_moves(snake.get_head())
        alive_moves = {move : potential_moves[move] for move in potential_moves 
                       if board.collision_check(potential_moves[move], snake.get_id())==False}
        best_move = False
        eval_new_state = []
        
        is_self = snake.get_id() == board.get_self_id()
        
        # If first turn - body usually doubled up
        if len(snake.body) != len(list(unique_everseen(snake.body))):
            snake.body = list(unique_everseen(snake.body))
            board.snakes[snake.get_id()].body = snake.body
            return self.minimax(board, snake, 0)
        
        for move in alive_moves:
            if print_output:
                if is_self:
                    print("\n___________________ ")
                print("\n" + snake.get_id(), move, "board")
                print("DEPTH:", depth)
            new_board = copy.deepcopy(board)
            snakes = new_board.get_snakes()
            new_board.move(snake.get_id(), alive_moves[move])
            if print_output:
                new_board.print_board()
            move_snake = new_board.snakes[snake.get_id()]
            
            # If snake is self, get move evals for other snakes
            if is_self:
                for snake_id in snakes:
                    if snake_id != move_snake.get_id():
                        enemy_snake = new_board.snakes[snake_id]
                        snake_move = self.minimax(new_board, enemy_snake, 0)
                        
                        enemy_potential_moves = new_board.find_moves(enemy_snake.get_head())
                        new_board.move(snake_id, enemy_potential_moves[snake_move[0]])
            
            # If not self, just eval and return
            
            # Scoring to be evaluated, is before board update so that food evaluation works
            self_score = self.evaluate_state(new_board, move_snake, print_output)
            new_board.update_board_after_move()
            
            
            # We want to maximize our score
            if is_self:
                # If depth is > 0, then minimax. Otherwise, return score
                if depth > 0:
                    eval_new_state = self.minimax(new_board, move_snake, depth-1)
                else:
                    eval_new_state = [move, self_score]
        
                # If best move exists, then compare it to new eval. If new eval is greater,
                # It becomes new best eval
                if best_move:
                    
                    if eval_new_state[1] > best_move[1]:
                        best_move = [move, eval_new_state[1]]
                else:
                    best_move = [move, eval_new_state[1]]
                    
            # Enemy wants to minimize our score
            else:
                # No need for minimax, just evaluate and compare
                eval_new_state = [move, self_score]
                
                if best_move:
                    if eval_new_state[1] < best_move[1]:
                        best_move = [move, eval_new_state[1]]
                else:
                    best_move = [move, eval_new_state[1]]
                
            
        # best_move[1] = best_move[1] + eval_state
        # print("State eval:", best_move[1])
        
        # Best move is list of form [direction, direction_value]
        return best_move
                    
                    
    def evaluate_state(self, board, snake, print_output = False): 
        # TODO: Minus score for collision unless it's a safe head to head, plus score for winning
        
         # Get moves where snake survives
        potential_moves = board.find_moves(snake.get_head())
        alive_moves = {move : potential_moves[move] for move in potential_moves 
                       if board.collision_check(potential_moves[move], snake.get_id())==False}
        
        # Set score to a 50
        # score = random.randint(50,51)
        score = 1
        position = snake.get_head()
        
        score += (10*len(alive_moves))
        
        # Increase score for health
        # score += self.bucket_health(snake.get_health(), 50)
        
        # Increase score for distance to food based on health
        if board.has_food() == True:
            food_dist = board.food_dist_pos(position)
            # print("Food dist:",food_dist)
            
            if snake.get_health() > 80:
                pass
            elif 30 < snake.get_health() < 80:
                if food_dist == 0: # or snake.get_head() == board.recently_removed_food:
                    score += 50
                elif food_dist < 3:
                    score += (30/int(food_dist))
                else:
                    score += self.bucket_food_dist(food_dist, board, max= 10)
            elif snake.get_health() < 30:
                if food_dist == 0: # or snake.get_head() == board.recently_removed_food:
                    score += 1000
                elif food_dist < (board.width/board.height)/5:
                    score += (50/int(food_dist))
                else:
                    score += self.bucket_food_dist(food_dist, board, max= 30)
                    
            # Increase food score if not largest length
            if board.relative_length(snake.get_id()) != 0:
                if food_dist == 0:
                    score += 1000
                elif food_dist < 10:
                    score += (50/int(food_dist))
                else:
                    score += self.bucket_food_dist(food_dist, board, max= 30)

        # Decrease score if near enemy snake head
        # enemy_near_count = 0
        # for enemy_snake in board.get_other_snakes(snake.get_id()):
        #     enemy_moves = board.find_moves(board.snakes[enemy_snake].get_head())
        #     for enemy_move in enemy_moves.values():
        #         if enemy_move in alive_moves.values():
        #             if board.snakes[enemy_snake].get_length() >= snake.get_length():
        #                 enemy_near_count += 1
        
        # score -= (enemy_near_count * 100)
            
        # Decrease score for number of enemies
        kill_value = 100
        other_snakes = board.get_other_snakes(snake.get_id())
        if print_output:
            score -= len(other_snakes)*kill_value
        
        print("Score: " + str(score))
        return score
    
    def bucket_food_dist(self, score, board, max= 50, bc= 10):
        max_score = max
        bucket_count = bc
        
        width = board.get_width()
        height = board.get_height()
        diagonal = width+height

        for bucket_num in range(1,bucket_count+1):
            if score <=(diagonal/bucket_count)*bucket_num:
                return max_score/bucket_num
        return 0
    
    def bucket_health(self, health, max= 50, bc= 5):
        max_score = max
        bucket_count = bc
        
        max_health = 100
        
        for bucket_num in range(1, bucket_count+1):
            if health <= (max_health/bucket_count)*bucket_num:
                return (max_score/bucket_count)*bucket_num
            
        return 0