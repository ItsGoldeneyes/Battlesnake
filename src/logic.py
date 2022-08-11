from snake import BattleSnake
from board import Board

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
        #Get Floodfill scores
        flood_scores = {move:self.flood_fill(self.board, alive_moves[move], []) for move in alive_moves}
        
        if self.board.get_health(self.id) < 30:
            food_dists = self.board.food_dist(self.get_head(), alive_moves)
            move_choice = min(food_dists, key=food_dists.get)
            if flood_scores[move_choice] < flood_scores[max(flood_scores, key=flood_scores.get)]/2:
                return max(flood_scores, key=flood_scores.get)
        
        return max(flood_scores, key=flood_scores.get)