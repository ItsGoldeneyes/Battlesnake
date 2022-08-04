#from board import board


class BattleSnake:
    
    def __init__(self, head, body, board):
        self.head = head
        self.body = body
        self.board = board
        
    def set_head(self, head):
        self.head = head
    
    def get_head(self):
        return self.head
    
    def set_body(self, body):
        self.body = body
    
    def get_body(self):
        return self.body
    
    def set_board(self, board):
        self.board = board
    
    def get_board(self):
        return self.board
    
    def set_position(self, snake_id, move, didEat=False):
        self.board.set_position(snake_id, move, didEat) 
        self.head, self.body = self.board.get_position(snake_id)
    
    def find_moves(self, position):
        return {
            "up": {"x": position['x'], "y": position['y']+1},
            "down": {"x": position['x'], "y": position['y']-1},
            "right": {"x": position['x']+1, "y": position['y']},
            "left": {"x": position['x']-1, "y": position['y']}
        }
    
    def collision_check(self, move):
        # 1. Check board borders
        if -1 == move["x"] or move["x"] >= self.board.get_width():
            # print(" -- Horizontal Wall collision")
            return True
        
        if -1 == move["y"] or move["y"] >= self.board.get_height():
            # print(" -- Vertical Wall collision")
            return True
        
        # 2. Check snakes
        if move in self.board.get_other_snakes():
            # print(" -- Snake collision")
            return True
        
        # 3. Check hazards
        if move in self.board.get_hazards():
            # print(" -- Hazard collision")
            return True

        return False
    
    def choose_move(self):
        moves = self.find_moves(self.get_head())
        moves = {move for move in moves if self.collision_check(move)==False}