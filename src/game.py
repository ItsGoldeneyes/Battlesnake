from snake import BattleSnake
from board import Board



class Game:
    def __init__(self, data):
        self.game_id = data["game"]["id"]
        self.board = Board(data)
        self.snakes = {snake["id"] : BattleSnake(self.board) for snake in data["board"]["snakes"]}
        self.self_id = data["you"]["id"]
        self.possible_moves = ["up", "down", "left", "right"]
        
    def get_id(self):
        return self.game_id
    
    def get_rules(self):
        return self.board.get_rules()
    
    def get_snakes(self):
        return self.snakes    

    def turn(self, data):
        board = Board(data)
        
        self.snakes[self.self_id].board_update(board)
        move = self.snakes[self.self_id].choose_move()
        if move in self.possible_moves and move != None:
            return move
        else:
            print(move)
            return "up"