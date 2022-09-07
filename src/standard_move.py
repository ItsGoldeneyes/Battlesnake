from minimax_std import Minimax

class StandardMove:
    def __init__(self, board):
        self.board = board

    def choose_move(self, self_snake, depth = 2):
        mm = Minimax()
        move = mm.minimax(self.board, self_snake, depth)
        print(move)
        return move[0]
        
        
        # No minimax
        # move_scores = self.evaluate_state_moves(self.board, self_snake)
        # if len(move_scores) != 0:
        #     return max(move_scores, key=move_scores.get)
        # else:
        #     return "up"
        
        
        # potential_moves = self.board.find_moves(self_snake.get_head())
        # #Filter collision moves
        
        # alive_moves = {move : potential_moves[move] for move in potential_moves 
        #                if self.board.collision_check(potential_moves[move])==False}
        
        # if alive_moves == {}:
        #     return "up"
        
        # move_choice = {}
        # flooder = Floodfill()
        
        # flood_scores = {move:flooder.flood_fill(self.board, alive_moves[move], []) 
        #                 for move in alive_moves}
        
        # # If coming up to intersection
        # if len(set(flood_scores.values())) != 1:
        #     print("flood:", flood_scores)
        #     move_choice = max(flood_scores, key=flood_scores.get)
        
        # # Avoid food if can
        # # elif self.board.get_health(self_snake.id) > 50:
        # #     no_food_moves = {move : potential_moves[move] for move in potential_moves 
        # #         if self.board.is_food(potential_moves[move])==False and 
        # #             self.board.collision_check(potential_moves[move])==False}
        # #     if no_food_moves != {}:
        # #         alive_moves = no_food_moves
        # #     move_choice = random.choice(list(alive_moves.keys()))  
                
        # else:
        #     move_choice = random.choice(list(alive_moves.keys()))
        
        # # If hungry    
        # if self.board.get_health(self_snake.id) < 20:
        #     food_dists = self.board.food_dist(self_snake.get_head(), alive_moves)
        #     if len(set(food_dists.values())) != 1:
        #         move_choice = min(food_dists, key=food_dists.get)
        # print(move_scores[max(move_scores, key=move_scores.get)])
