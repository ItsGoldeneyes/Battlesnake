from copy import copy, deepcopy
import funcs.snake

'''
Board format is a dictionary with the following keys:
    'height': The height of the board.
    'width': The width of the board.
    'food': A list of coordinates representing the food on the board.
    'hazard': A list of coordinates representing the hazards on the board.
    'hazard_damage': The amount of damage a snake takes when it collides with a hazard.
    'snakes': A list of snake objects.
'''

def make_move(board, snake_id, move) -> dict:
    '''
    Make a move on the board.
    Change the board parameter and return a state dictionary.
    The state dictionary should contain the following keys:
        'snake': The main snake's body before the move.
        'food': Coordinates of any removed food.
    '''
    print("snake_id: ", snake_id)
    state = {
        'snake': deepcopy(board['snakes'][snake_id]['body']),
        'food': food_check(board, snake_id)
    }

    board['snakes'][snake_id]['body'].insert(0, move)
    
    if not state['food']:
        board['snakes'][snake_id]['body'].pop()
    
    return state

def unmake_move(board, snake_id, state) -> None:
    '''
    Reset the board parameter to the state parameter.
    '''
    board['snakes'][snake_id]['body'] = state['snake']
    
    if state['food']:
        board['food'].append(state['snake'][0])
        
def get_state(board) -> dict:
    '''
    Return a state dictionary.
    The state dictionary should contain the following keys:
        'snake': The main snake's body before the move.
        'food': Coordinates of any removed food.
    '''
    state = deepcopy(board)
    
    return state

def reset_state(board, state) -> None:
    '''
    Reset the board parameter to the state parameter.
    '''
    board = state

def food_check(board, snake_id) -> bool:
    '''
    Check for food collisions on the board.
    Return True or False
    '''
    if board.get('food'):
        if board['snakes'][snake_id]['head'] in board['food']:
            return True
    return False

def dict_next_key(dictionary, key):
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
    
def get_move(board, snake_id, dir):
    if dir == "up":
        return board[snake_id]['head'][0], board[snake_id]['head'][1] + 1
    elif dir == "down":
        return board[snake_id]['head'][0], board[snake_id]['head'][1] - 1
    elif dir == "left":
        return board[snake_id]['head'][0] - 1, board[snake_id]['head'][1]
    elif dir == "right":
        return board[snake_id]['head'][0] + 1, board[snake_id]['head'][1]
    
def collision_check(board, snake_id) -> int:
    '''
    Check for collisions on the board.
    Return a value based on the collision type
    '''
    pass

def head_collision_check(board, snake_id) -> bool:
    '''
    Check for head collisions on the board.
    Return True or False
    '''
    pass

def body_collision_check(board, snake_id) -> bool:
    '''
    Check for body collisions on the board.
    Return True or False
    '''
    pass

def wall_collision_check(board, snake_id) -> bool:
    '''
    Check if snake is out of bounds
    Return True or False
    '''
    pass
    
def hazard_collision_check(board, snake_id) -> bool:
    '''
    Check for hazard collisions
    Return True or False
    '''