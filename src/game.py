from standard.standard_move import StandardMove
from wrapped.wrapped_move import WrappedMove
from board import Board
import random


class Game:
    def __init__(self, data):
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
        # # self.board.print_board()
        
        if self.rules == "standard":
            print('Standard move')
            move_type = StandardMove(self.board)
            move = move_type.choose_move(self.board.snakes[self.board.get_self_id()], depth= 3)
        
        elif self.rules == "wrapped":
            print('Wrapped move')
            move_type = WrappedMove(self.board)
            move = move_type.choose_move(self.board.snakes[self.board.get_self_id()], depth= 3)
        # if self.rules == "solo":
        #     move_type = StandardMove(self.board)
        #     move = move_type.choose_move(self.board.snakes[self.board.get_self_id()], depth= 2)
        
        # elif self.map == "arcade_maze":
        #    move_type = MazeMove(self.board)
        #    move = move_type.choose_move(self.board.snakes[self.board.get_self_id()], depth= 2)
        
        else:
            move_type = StandardMove(self.board)
            move = move_type.choose_move(self.board.snakes[self.board.get_self_id()], depth= 2)
            # potential_moves = self.board.find_moves(self.get_head())
            # alive_moves = {move : potential_moves[move] for move in potential_moves if self.board.collision_check(potential_moves[move])==False}
            # if alive_moves == {}:
            #     return "up"
            # if self.board.get_health(self.id) < 30:
            #     food_dists = self.board.food_dist(self.get_head(), alive_moves)
            #     move_choice = min(food_dists, key=food_dists.get)
            # else:
            #     move_choice = random.choice(list(alive_moves.keys()))
            # move = move_choice
        
        if move in self.possible_moves and move != None:
            return move
        else:
            print("INCORRECT MOVE FORMAT:", move)
            return self.board.find_moves(self.board.snakes[self.board.get_self_id()].get_head())
            # return "up"