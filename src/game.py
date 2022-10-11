from gamemodes.standard_move import StandardMove
from gamemodes.wrapped_move import WrappedMove
from board import Board


class Game:
    '''
    This class is a Game object that contains all the information about a game.
    Not much logic is done here aside from choosing the game type each turn.
    It contains the active board as well as the map and rules.
    '''
    def __init__(self, data, debug_mode= False):
        self.debug_mode = debug_mode
        
        self.game_id = data["game"]["id"]
        self.self_id = data["you"]["id"]
        self.map = data["game"]["map"]
        self.rules = data["game"]["ruleset"]["name"]
        self.board = Board(data)
                
        self.possible_moves = ["up", "down", "left", "right"]
        
        print(self.rules, flush= True)
        
    def get_id(self):
        return self.game_id
    
    def get_rules(self):
        return self.rules
    
    def get_snakes(self):
        return self.board.snakes

    def turn(self, data):
        self.board = Board(data)
        if self.debug_mode:
            self.board.print_board()
        
        if self.rules == "standard":
                move_type = StandardMove(self.board, debug_mode= self.debug_mode)
                move = move_type.choose_move(self.board.snakes[self.board.get_self_id()], depth= 4)
        
        elif self.rules == "wrapped":
                move_type = WrappedMove(self.board, debug_mode= self.debug_mode)
                move = move_type.choose_move(self.board.snakes[self.board.get_self_id()], depth= 4)
            
        elif self.rules == "solo":
            move_type = StandardMove(self.board, debug_mode= self.debug_mode)
            move = move_type.choose_move(self.board.snakes[self.board.get_self_id()], depth= 4)
        
        else:
            move_type = StandardMove(self.board, debug_mode= self.debug_mode)
            move = move_type.choose_move(self.board.snakes[self.board.get_self_id()], depth= 2)
            
        
        if move in self.possible_moves and move != None:
            return move
        else:
            print("INCORRECT MOVE FORMAT:", move)
            # return self.board.find_moves(self.board.snakes[self.board.get_self_id()].get_head())
            return "up"