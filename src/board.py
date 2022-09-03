from snake import BattleSnake
import numpy as np
import math


class Board:
    
    def __init__(self, data):
        self.data = data
        self.board = data["board"]
        self.width = self.board["width"]
        self.height = self.board["height"]
        
        self.hazards = self.board["hazards"]
        self.food = self.board["food"]
        
        self.snakes = {snake["id"] : BattleSnake(self, snake["id"]) for snake in self.board["snakes"]}
    
    def clone(self):
        return Board(self.data)
    
    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_hazards(self):
        return self.hazards
        
    def get_food(self):
        return self.food
    
    def get_snakes(self):
        return self.snakes 
    
    def get_self_id(self):
        return self.data["you"]["id"]
    
    def get_position(self, id):
        return self.snakes[id]["head"], self.snakes[id]["body"]
    
    def get_health(self, id):
        return self.snakes[id]["health"]
    
    def get_length(self, id):
        return self.snakes[id]["length"]
    
    def point_to_list(self, point):
        return [point["x"],point["y"]]
    
    def get_snake_collision(self, id):
        snakes_hitbox = []
        for snake_id in self.snakes:
            snakes_hitbox.extend(self.snakes[snake_id].get_body())
            if snake_id == id:
                snakes_hitbox.pop(self.snakes[snake_id].get_head())
        return snakes_hitbox
    
    def print_board(self):
        board_array = [[] for i in range(self.height)]
        for y_pos in range(self.height):
            for x_pos in range(self.width):
                coord = {"x": x_pos, "y": y_pos}
                # Check for food
                if coord in self.food:
                    board_array[y_pos].append("F")
                # Check for hazards
                elif coord in self.hazards:
                    board_array[y_pos].append("X")
                # Check for snakes
                elif coord in self.snakes_hitbox: # Fix with get snake collision
                    board_array[y_pos].append("O")
                # Empty space
                else:
                    board_array[y_pos].append("◦")
        board_array.reverse()
        for col in board_array:
            for elem in col:
                print(elem, end=" ")
            print("")
            # print(col)
            
    def find_moves(self, position):
        return {
            "up": {"x": position['x'], "y": position['y']+1},
            "down": {"x": position['x'], "y": position['y']-1},
            "right": {"x": position['x']+1, "y": position['y']},
            "left": {"x": position['x']-1, "y": position['y']}
        }
       
       
    def move(self, snake_id, move):
        self.snakes[snake_id].head = move
        self.snakes[snake_id].body.insert(0, move)
        if move not in self.get_food():
            self.snakes[snake_id].body.pop()
        else:
            self.food.remove(move)
        
    
    def fake_move(self, snake_id):
        self.snakes[snake_id].body.insert(0, self.snakes[snake_id]["head"])
        self.snakes[snake_id].body.pop()
        
                
    def collision_check(self, move, id):
        # 1. Check board borders
        if -1 == move["x"] or move["x"] >= self.width:
            # print(" -- Horizontal Wall collision")
            return True
        
        if -1 == move["y"] or move["y"] >= self.height:
            # print(" -- Vertical Wall collision")
            return True
        
        # 2. Check snakes
        if move in self.get_snake_collision(id):
            # print(" -- Snake collision")
            return True
        
        # 3. Check hazards
        if move in self.hazards:
            # print(" -- Hazard collision")
            return True
        return False
    
    
    def avoid_food(self, move):
        if move in self.food:
            return True
        return False
    
    
    def closest_food(self, point_dict):
        food_list = np.array([self.point_to_list(point) for point in self.food])
        point = np.array([self.point_to_list(point_dict)])
        
        distances = np.linalg.norm(food_list-point, axis=1)
        min_index = np.argmin(distances)
        return food_list[min_index]
        
    def food_dist_pos(self, pos):
        if self.food == []:
            score = 0
            return score

        food = self.closest_food(pos)
        score = math.sqrt(((pos["x"]-food[0])**2) + ((pos["y"]-food[1])**2))
        return score
    
    def food_dist_moves(self, head, move_dict): 
        if self.food == []:
            scores = {move:0 for move in move_dict}
            return scores

        food = self.closest_food(head)
        scores = {}
        for move in move_dict:
            val = math.sqrt(((move_dict[move]["x"]-food[0])**2) + ((move_dict[move]["y"]-food[1])**2))
            scores[move] = val
        return scores
    
    def update_board_after_move(self):
        # Lowers HP, remove dead snakes
        new_snakes = dict(self.snakes)
        for snake_id in self.snakes:
            if self.collision_check_not_new(new_snakes[snake_id]["head"], snake_id) or new_snakes[snake_id]["health"] <= 0:
                new_snakes.pop(snake_id)
            else:
                new_snakes[snake_id].health = new_snakes[snake_id].health - 1
        self.snakes = dict(new_snakes)