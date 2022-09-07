import random

class Minimax:    
    def minimax(self, board, snake, depth= 2):
        eval_state = self.evaluate_state(board, snake)
        potential_moves = board.find_moves(snake.get_head())
        alive_moves = {move : potential_moves[move] for move in potential_moves 
                       if board.collision_check(potential_moves[move], snake.get_id())==False}
        best_move = False
        eval_new_state = []
        
        # print("start")
        if len(alive_moves) == 0:
            return ["up", -1000]
        
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
                        
                        enemy_potential_moves = board.find_moves(enemy_snake.get_head())
                        new_board.move(snake_id, enemy_potential_moves[snake_move[0]])
                        
            # If deciding for other snakes, prevent infinite loop            
            else:
                # print("other snake")
                for snake_id in snakes:
                    new_board.fake_move(snake_id)
            
            # print('update_board')
            # new_board.update_board_after_move()
            
            if depth > 0:
                eval_new_state = self.minimax(new_board, move_snake, depth-1)
            else:
                #Format to [move, value] for return
                eval_new_state = [move, self.evaluate_state(new_board, move_snake)]
            
            if best_move:
                if eval_new_state[1] > best_move[1]:
                    best_move = [move, eval_new_state[1]]
            else:
                best_move = [move, eval_new_state[1]]
            
        best_move[1] = best_move[1] + eval_state
        
        return best_move
                    
                    
    def evaluate_state(self, board, snake): 
         # Get moves where snake survives
        potential_moves = board.find_moves(snake.get_head())
        alive_moves = {move : potential_moves[move] for move in potential_moves 
                       if board.collision_check(potential_moves[move], snake.get_id())==False}
        
        # Set score to a 50
        score = random.randint(49,51)
        # score = 1
        position = snake.get_head()
        
        # Increase score for health
        # score += self.bucket_health(snake.get_health(), 50)
        
        # Increase score for distance to food based on health
        food_dist = board.food_dist_pos(position)
        if snake.get_health() > 80:
            pass
        elif 30 < snake.get_health() < 80:
            if food_dist < 5:
                score += 30
            else:
                score += self.bucket_food_dist(food_dist, board, max= 20)
        elif snake.get_health() < 30:
            if food_dist == 0:
                score += 100
            elif food_dist < 10:
                score += (90/food_dist)
            else:
                score += self.bucket_food_dist(food_dist, board, max= 50)

        # Increase score if not largest length
        if board.relative_length(snake.get_id()) != 0:
            if food_dist == 0:
                score += 100
            elif food_dist < 10:
                score += (90/food_dist)
            else:
                score += self.bucket_food_dist(food_dist, board, max= 50)

            # Decrease score if near enemy snake head
            enemy_near_count = 0
            for enemy_snake in board.get_other_snakes(snake.get_id()):
                enemy_moves = board.find_moves(board.snakes[enemy_snake].get_head())
                for enemy_move in enemy_moves.values():
                    if enemy_move in alive_moves.values():
                        enemy_near_count += 1
            
            score -= (enemy_near_count * 50)
            
        # Decrease score for number of enemies
        kill_value = 100
        other_snakes = board.get_other_snakes(snake.get_id())
        score = score - len(other_snakes)*kill_value
            
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