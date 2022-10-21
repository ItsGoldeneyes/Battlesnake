'''
This file contains useful functions for a standard BattleSnake game.

'''

def standard_eval(board, snake_id, food_count= 0): 
    '''
    This function is the standard evaluation function.
    It takes a board and a snake and returns the evaluation for that snake.
    
    TODO: incentivize murder
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
    
    if board.body_collision_check(snake_pos):
        return -100
    
    if board.wall_collision_check(snake_pos):
        return -100

    if board.hazard_collision_check(snake_pos):
        return -100

    # Base score
    score = 0
    position = snake.get_head()
    
    score += food_count
    # Increase score for health
    if snake.get_health() > 50:
        score += 0.2
            
    # Increase score for distance to food based on health
    if board.has_food() == True:
        food_dist = board.food_dist(position)
        
        if food_dist < (board.get_width()/board.get_height())/5:
            score += (0.5/int(food_dist))
        else:
            score += bucket_food_dist(food_dist, board, max= 0.3)
                
        # Increase food score if not largest length
        if board.relative_length(snake.get_id()) != 0:
            if food_dist < (board.get_width()/board.get_height())/5:
                score += (0.5/int(food_dist))
            else:
                score += bucket_food_dist(food_dist, board, max= 0.3)
                
    # Decrease score for each enemy snake    
    score -= (len(board.snakes)-1)/2
    
    return score