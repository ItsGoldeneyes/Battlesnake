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
    
    def get_id(self) -> str:
        '''
        Return the game id.
        '''
        pass
    
    def save_game(self) -> bool:
        '''
        Save the game to a file.
        '''
        pass
    
    def pull_data(self, data) -> dict:
        '''
        Pull board and snake data from request
        '''
        snakes = {}
        
        snakes[data['you']['id']] = {'id': data['you']['id'],
                'head': data['you']['head'],
                'body': data['you']['body'],
                'health': data['you']['health']
        }
            
        for snake in data['board']['snakes']:
            if snake['id'] == data['you']['id']:
                continue
            snakes[snake['id']] = {
                'id': snake['id'],
                'head': snake['head'],
                'body': snake['body'],
                'health': snake['health'],
            }
        
        board = {
            'height': data['board']['height'],
            'width': data['board']['width'],
            'food': data['board']['food'],
            'hazards': data['board']['hazards'],
            'hazard_damage': data['game']['ruleset']['settings']['hazardDamagePerTurn'],
            'snakes': snakes,
        }
        
        return board
        
    def turn(self, data) -> str:
        '''
        Process the current turn data and return the next move.
        '''
        board = self.pull_data(data)
        
        
        pass