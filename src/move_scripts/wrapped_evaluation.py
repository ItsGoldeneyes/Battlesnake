
def evaluate_state(self, board, snake, debug_mode = False): 
    # TODO: Minus score for collision unless it's a safe head to head, prioritize winning
    
        # Get moves where snake survives
    potential_moves = board.find_moves(snake.get_head())
    alive_moves = {move : potential_moves[move] for move in potential_moves 
                    if board.collision_check(potential_moves[move], snake.get_id())==False}
    
    if board.collision_check(snake.get_head(), snake.get_id()) and board.near_tail(snake.get_head())==False:
        return -100
    
    if len(alive_moves) == 0:
        return -100

    # Base score
    score = 0
    position = snake.get_head()
    
    # Increase score for health
    if 95 <= snake.get_health() <= 100:
        score += 1
    # score += self.bucket_health(snake.get_health(), 2)
    
    # Increase score for distance to food based on health
    if board.has_food() == True:
        food_dist = board.food_dist(position)
        # print("Food dist:",food_dist)
        if snake.get_health() > 80:
            pass
        
        elif 30 < snake.get_health() < 80:
            if food_dist == 0:
                score += 1
            elif food_dist < 3:
                score += 0.5
            else:
                score += self.bucket_food_dist(food_dist, board, max= 0.5)
                
        elif snake.get_health() < 30:
            # if food_dist == 0: # or snake.get_head() == board.recently_removed_food:
            #     score += 3
            # el
            if food_dist < (board.width/board.height)/5:
                score += (1/int(food_dist))
            else:
                score += self.bucket_food_dist(food_dist, board, max= 1)
                
        # Increase food score if not largest length
        if board.relative_length(snake.get_id()) != 0:
            if food_dist == 0:
                score += 1
            elif food_dist < 10:
                score += (1/int(food_dist))
            else:
                score += self.bucket_food_dist(food_dist, board, max= 1)
    
    
    # Increase or decrease if move is possible move of other snake
    for enemy_snake_id in board.get_other_snakes(snake.get_id()):
        if board.near_head(enemy_snake_id, snake.get_id()):
            if snake.get_length() > board.snakes[enemy_snake_id].get_length():
                score += 0.5
            else:
                score -= 2
            
    
    # score -= (enemy_near_count * 100)
        
    # Decrease score for number of enemies
    # kill_value = 100
    # other_snakes = board.get_other_snakes(snake.get_id())
    # score -= len(other_snakes)*kill_value            
    
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

def bucket_health(self, health, max= 50, bc= 10):
    max_score = max
    bucket_count = bc
    
    max_health = 100
    
    for bucket_num in range(1, bucket_count+1):
        if health <= (max_health/bucket_count)*bucket_num:
            return (max_score/bucket_count)*bucket_num
        
    return 0