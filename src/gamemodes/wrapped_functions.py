
'''
This file contains useful functions for a wrapped BattleSnake game.

'''

def wrapped_eval(board, snake): 
    '''
    This function is the wrapped evaluation function.
    It takes a board and a snake and returns the evaluation for that snake.
    '''
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
    
    # Get moves where snake survives
    # potential_moves = board.find_moves(snake.get_head())
    # alive_moves = {move : potential_moves[move] for move in potential_moves 
    #                 if board.collision_check(potential_moves[move], snake.get_id())==False}
    
    if board.collision_check(snake.get_head(), snake.get_id()):
        if board.on_tail(snake.get_head()):
            return 0.5
        return -100
    
    # if len(alive_moves) == 0:
    #     return -100

    # if board.near_tail(snake.get_head()):
    #     return -20
    

    # Base score
    score = 0
    position = snake.get_head()
    
    # Increase score for health
    if 95 <= snake.get_health() <= 100:
        score += 1
    # score += bucket_health(snake.get_health(), 2)
    
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
                score += (0.9/int(food_dist))
            else:
                score += bucket_food_dist(food_dist, board, max= 0.5)
                
        # Increase food score if not largest length
        if board.relative_length(snake.get_id()) != 0:
            if food_dist == 0:
                score += 1
            elif food_dist < 10:
                score += (0.9/int(food_dist))
            else:
                score += bucket_food_dist(food_dist, board, max= 0.5)
    
    # if len(board.snakes) == 1:
    #     score += 1
    
    return score

