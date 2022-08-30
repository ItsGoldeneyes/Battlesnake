from floodfill_board import floodfill as ff
import random

class StandardMove:
    def __init__(self, board):
        self.board = board

    def choose_move(self, self_snake):
        move_scores = self.evaluate_state(self_snake)
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
        # #         if self.board.avoid_food(potential_moves[move])==False and 
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
        if len(move_scores) != 0:
            return max(move_scores, key=move_scores.get)
        else:
            return "up"
        

    
    def add_scores(self, scores, additional_scores):
        new_scores = {}
        for key in scores.keys():
            if key in additional_scores.keys():
                new_scores[key] = scores[key] + additional_scores[key]
            else:
                new_scores[key] = scores[key]
            
        return new_scores

    def evaluate_state(self, self_snake):
        # Get moves where snake survives
        potential_moves = self.board.find_moves(self_snake.get_head())
        alive_moves = {move : potential_moves[move] for move in potential_moves 
                       if self.board.collision_check(potential_moves[move])==False}
        
        # Set scores to a random number between 1 and 5
        scores = {move : random.randint(1,4)*0.25 for move in potential_moves 
                       if self.board.collision_check(potential_moves[move])==False}
        
        # If a collision happens, floodfill
        if len(alive_moves) < 3:
            value_divide = 100
            flooder = ff() # Remove this line when able to do without object
            flood_amt = {move:flooder.floodfill(self.board, alive_moves[move], [])/value_divide 
                         for move in alive_moves}
            if len(set(flood_amt.values())) != 1:
                flood_scores = {}
                pos = 1
                for move in sorted(flood_amt, key=flood_amt.get, reverse=True):
                    flood_scores.update({move: value_divide/pos})
                scores = self.add_scores(scores, flood_scores)
                print(scores)
            
        # Decrease value if snake not hungry
        if self.board.get_health(self_snake.id) > 90:
            value_add = -10
            no_food_moves = {move : potential_moves[move] for move in potential_moves 
                if self.board.avoid_food(potential_moves[move])==False and 
                    self.board.collision_check(potential_moves[move])==False}
            
            if no_food_moves != {}:
                no_food_scores = {move : value_add for move in alive_moves if move not in no_food_moves}
                scores = self.add_scores(scores, no_food_scores)
                print(scores)
        
        # Increase value if Snake is hungry
        elif self.board.get_health(self_snake.id) < 20:
            value_to_divide = 30
            food_dists = self.board.food_dist(self_snake.get_head(), alive_moves)
            if len(set(food_dists.values())) != 1:
                food_scores = {}
                pos = 1
                for move in sorted(food_dists, key=food_dists.get, reverse=False):
                    food_scores.update({move: value_to_divide/pos})
                    pos += 1
                scores = self.add_scores(scores, food_scores)
            print(scores)
                
                
                
        return scores