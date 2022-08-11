from board import Board
import random


class BattleSnake:
    
    def __init__(self, board):
        self.set_board(board)
        self.set_id(board.get_player_id())
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
    
    def move(self, snake_id, move, did_eat=False):
        self.board.move(snake_id, move, did_eat) 
        self.head, self.body = self.board.get_position(snake_id)
    
    def find_moves(self, position):
        return {
            "up": {"x": position['x'], "y": position['y']+1},
            "down": {"x": position['x'], "y": position['y']-1},
            "right": {"x": position['x']+1, "y": position['y']},
            "left": {"x": position['x']-1, "y": position['y']}
        }
    
    def choose_move(self):
        potential_moves = self.find_moves(self.get_head())
        alive_moves = {move : potential_moves[move] for move in potential_moves if self.board.collision_check(potential_moves[move])==False}
        if self.board.get_health(self.id) < 30:
            food_dists = self.board.food_dist(self.get_head(), alive_moves)
            move_choice = min(food_dists, key=food_dists.get)
        else:
            move_choice = random.choice(list(alive_moves.keys()))
        return move_choice