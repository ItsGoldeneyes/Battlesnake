from board import Board
import random


class BattleSnake:
    
    def __init__(self, head, body, id, board):
        self.set_head(head)
        self.set_body(body)
        self.set_board(board)
        self.set_id(id)
        
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
        moves = self.find_moves(self.get_head())
        moves = [move for move in moves if self.board.collision_check(move)==False]
        random.choice(moves)