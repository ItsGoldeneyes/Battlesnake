from snake import BattleSnake
from board import Board
import random

class LogicSnake(BattleSnake):
    def __init__(self, board):
        super().__init__(board)
        
        
    def flood_fill(self, board, move, accessed = []):
        if board.collision_check(move):
            return 0
        
        accessed.append(move)
        total = 1
        for new_move in self.find_moves(move).values():
            if new_move not in accessed:
                total = total + self.flood_fill(board, new_move, accessed)
        return total
    
    
    def choose_move(self):
        potential_moves = self.find_moves(self.get_head())
        #Filter collision moves
        alive_moves = {move : potential_moves[move] for move in potential_moves 
                       if self.board.collision_check(potential_moves[move])==False}
        if alive_moves == {}:
            return "up"
        
        move_choice = {}
        flood_scores = {move:self.flood_fill(self.board, alive_moves[move], []) for move in alive_moves}
        
        if len(set(flood_scores.values())) != 1:
            print("flood:", flood_scores)
            move_choice = max(flood_scores, key=flood_scores.get)
        
        # Avoid food if can
        elif self.board.get_health(self.id) > 50:
            no_food_moves = {move : potential_moves[move] for move in potential_moves 
                if self.board.avoid_food(potential_moves[move])==False}
            if no_food_moves != {}:
                alive_moves = no_food_moves
                
        else:
            move_choice = random.choice(list(alive_moves.keys()))
            
        if self.board.get_head(self.id) < 10:
            food_dists = self.board.food_dist(self.get_head(), alive_moves)
            if len(set(food_dists.values())) != 1:
                move_choice = min(food_dists, key=food_dists.get)
        
        print(move_choice)
        print("")
        return move_choice