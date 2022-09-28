class floodfill:
    def __init__(self):
        self.accessed = []
        
    def floodfill(self, board, move, snake_id):
        if board.collision_check(move, snake_id):
            return 0
        
        self.accessed.append(move)
        total = 1
        for new_move in board.find_moves(move).values():
            if new_move not in self.accessed:
                total = total + self.floodfill(board, new_move, snake_id)
        return total