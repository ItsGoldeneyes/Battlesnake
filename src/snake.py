from standard_move import StandardMove

import random


class BattleSnake:
    
    def __init__(self, board, id=""):
        if id == "":
            id = board.get_self_id()
            
        self.set_board(board)
        self.set_id(id)
        self.head, self.body = self.board.get_position(self.id)
        
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
    
    def set_id(self, id):
        self.id = id
    
    def get_id(self):
        return self.id
    
    def board_update(self, board):
        self.set_board(board)
        self.head, self.body = self.board.get_position(self.id)
    
    def clone(self, board):
        return BattleSnake(board)
    
    def move(self, snake_id, move, did_eat=False):
        self.board.move(snake_id, move, did_eat) 
        self.head, self.body = self.board.get_position(snake_id)
    
    def choose_move(self):
        if self.board.get_rules() == "standard" or "solo":
            standard_move = StandardMove(self.board)
            move = standard_move.choose_move(self)
            
        else: 
            potential_moves = self.board.find_moves(self.get_head())
            alive_moves = {move : potential_moves[move] for move in potential_moves if self.board.collision_check(potential_moves[move])==False}
            if alive_moves == {}:
                return "up"
            if self.board.get_health(self.id) < 30:
                food_dists = self.board.food_dist(self.get_head(), alive_moves)
                move_choice = min(food_dists, key=food_dists.get)
            else:
                move_choice = random.choice(list(alive_moves.keys()))
            move = move_choice
            
        return move