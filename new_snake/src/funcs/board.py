'''
Board format is a dictionary with the following keys:
    'height': The height of the board.
    'width': The width of the board.
    'food': A list of coordinates representing the food on the board.
    'hazard': A list of coordinates representing the hazards on the board.
    'hazard_damage': The amount of damage a snake takes when it collides with a hazard.
'''


def make_move(board, snake, move) -> dict:
    '''
    Make a move on the board.
    Change the board parameter and return a state dictionary.
    The state dictionary should contain the following keys:
        'snake': The main snake's body before the move.
        'food': Coordinates of any removed food.
    '''
    pass

def unmake_move(board, state) -> None:
    '''
    Reset the board parameter to the state parameter.
    '''
    pass

def food_check(board, snake) -> bool:
    '''
    Check for food collisions on the board.
    Return True or False
    '''
    pass

def collision_check(board, snake) -> int:
    '''
    Check for collisions on the board.
    Return a value based on the collision type
    '''
    pass