from src.snake import BattleSnake
from src.board import Board

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
        moves = {move : potential_moves[move] for move in potential_moves 
                       if self.board.collision_check(potential_moves[move])==False}
        #Get Floodfill scores
        flood_scores = [self.flood_fill(self.board, potential_moves[move]) for move in potential_moves]
        return flood_scores