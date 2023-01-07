import time

class SnakeGame:
    def __init__(self):
        '''
        Process the initial game data and set up the game.
        Start timers if needed.
        '''
        
        # Maybe?
        # if game.type == 'wrapped':
        #     self.turn = self.wrapped_turn 
        pass
    
    def get_id(self):
        '''
        Return the game id.
        '''
        pass
    
    def save_game(self):
        '''
        Save the game to a file.
        '''
        pass
    
    def pull_data(self):
        '''
        Pull board and snake data from request
        '''
    
    def turn(self, data):
        '''
        Process the current turn data and return the next move.
        '''
        board, snakes = self.pull_data(data)
        pass
    
    