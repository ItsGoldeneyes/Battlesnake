
'''
Snake format is a dictionary with the following keys:
    'id': The snake's unique identifier.
    'head': A coordinate representing the snake's head.
    'body': A list of coordinates representing the snake's body.
    'health': The snake's current health.
'''

def s_id(snake):
    '''
    Return the id of the snake.
    '''
    return snake['id']

def s_len(snake):
    '''
    Return the length of the snake.
    '''
    return len(snake['body'])

def s_head(snake):
    '''
    Return the head of the snake.
    '''
    return snake['body'][0]

def s_body(snake):
    '''
    Return the body of the snake.
    '''
    return snake['body']

def s_tail(snake):
    '''
    Return the tail of the snake.
    '''
    return snake['body'][1:]

def s_tail_tip(snake):
    '''
    Return the tail tip of the snake.
    ''' 
    return snake['body'][-1]