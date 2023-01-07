class floodfill:
    '''
    This class contains a floodfill function.
    This function checks the available area for a given move. 
    It seems to be very inefficient, I haven't put much into it.
    '''
    def __init__(self):
        self.accessed = []
        
    def floodfill(self, board, move, snake_id):
        if board.collision_check(move, snake_id):
            return 0
        
        self.accessed.append(move)
        total = 1
        for new_move in board.get_moves(move).values():
            if new_move not in self.accessed:
                total = total + self.floodfill(board, new_move, snake_id)
        return total