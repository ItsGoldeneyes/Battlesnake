'''
This file contains useful functions for a wrapped BattleSnake game.

'''

def wrapped_eval(board, snake_id): 
    '''
    This function is the wrapped evaluation function.
    It takes a board and a snake and returns the evaluation for that snake.
    
    TODO: Separate head collisions from self + wall. Hazards separate as well for battle royale
    incentivize murder
    '''
    if snake_id not in board.get_snakes():
        return -100
    def bucket_food_dist(score, board, max= 50, bc= 10):
        
        max_score = max
        bucket_count = bc
        
        width = board.get_width()
        height = board.get_height()
        diagonal = width+height

        for bucket_num in range(1, bucket_count+1):
            if score <=(diagonal/bucket_count)*bucket_num:
                return max_score/bucket_num
        return 0
    
    snake = board.get_snake(snake_id)
    snake_pos = snake.get_head()
    
    if board.head_collision_check(snake_pos, snake_id):
        return -50
    
    if board.body_collision_check(snake_pos, snake_id):
        return -100

    if board.hazard_collision_check(snake_pos, snake_id):
        return -100

    # Base score
    score = 0
    position = snake.get_head()
    
    # Increase score for health
    # if 95 <= snake.get_health() <= 100:
    #     score += 1
    # # score += bucket_health(snake.get_health(), 2)
    
    # Increase score for distance to food based on health
    if board.has_food() == True:
        food_dist = board.food_dist(position)
        # print("Food dist:",food_dist)
        if 98 <= snake.get_health() <= 100:
            score += 1
            
        elif snake.get_health() < 30:
            if food_dist == 0:
                score += 1
            elif food_dist < (board.width/board.height)/5:
                score += (0.5/int(food_dist))
            else:
                score += bucket_food_dist(food_dist, board, max= 0.3)
                
        # Increase food score if not largest length
        if board.relative_length(snake.get_id()) != 0:
            if food_dist == 0:
                score += 1
            elif food_dist < 10:
                score += (0.3/int(food_dist))
            else:
                score += bucket_food_dist(food_dist, board, max= 0.3)
    
    # Increase or decrease if move is possible move of other snake
    # for enemy_snake_id in board.get_other_snakes(snake.get_id()):
    #     if board.near_head(position, enemy_snake_id):
    #         # if snake.get_length() > board.snakes[enemy_snake_id].get_length():
    #         #     score += 0 #0.5
    #         # else:
    #        # print("true")
    #         score -= 5   
    return score

