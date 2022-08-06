from scipy.spatial import distance
import numpy as np
import math
import random


class Board:
    
    def __init__(self, data):
        self.data = data
        self.board = data["board"]
        self.width = self.board["width"]
        self.height = self.board["height"]
        
        self.hazards = data["board"]["hazards"]
        self.food = data["board"]["food"]
        
        self.snakes = {snake["id"] : snake for snake in self.board["snakes"]}
        self.update_snake_collision()
            
    def get_data(self):
        return self.data
    
    def get_board(self):
        return self.board
    
    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_hazards(self):
        return self.hazards
    
    def set_food(self, food):
        self.food = food
        
    def get_food(self):
        return self.food
    
    def get_snakes(self):
        return self.snakes 
    
    def get_player_id(self):
        return self.data["you"]["id"]     
    
    def point_to_list(self, point):
        return [point["x"],point["y"]]
    
    def update_snake_collision(self):
        self.snakes_hitbox = []
        for snake in self.snakes.keys():
            self.snakes_hitbox.extend(self.snakes[snake]["body"])
    
    def collision_check(self, move):
        # 1. Check board borders
        if -1 == move["x"] or move["x"] >= self.width:
            # print(" -- Horizontal Wall collision")
            return True
        
        if -1 == move["y"] or move["y"] >= self.height:
            # print(" -- Vertical Wall collision")
            return True
        
        # 2. Check snakes
        if move in self.snakes_hitbox:
            # print(" -- Snake collision")
            return True
        
        # 3. Check hazards
        if move in self.hazards:
            # print(" -- Hazard collision")
            return True
        return False
    
    def closest_food(self, point_dict):
        food_list = np.array([self.point_to_list(point) for point in self.food])
        point = np.array([self.point_to_list(point_dict)])
        
        distances = np.linalg.norm(food_list-point, axis=1)
        min_index = np.argmin(distances)
        return food_list[min_index]
        
    
    def prioritize_food(self, head, move_dict):
        print(move_dict)
        if self.food == []:
            return random.choice(list(move_dict.keys()))
        food = self.closest_food(head)
        max_dist = 999
        best_move = None
        for move in move_dict:
            move_list = self.point_to_list(move_dict[move])
            if math.dist(move_list,food) < max_dist:
                max_dist = math.dist(move_list,food)
                best_move = move
        return best_move
            
    def move(self, snake_id, move, did_eat = False):
        self.snakes[snake_id]["head"] = move
        self.snakes[snake_id]["body"].insert(0, move)
        if not did_eat:
            self.snakes[snake_id]["body"].pop()
        self.update_snake_collision()
        
    def get_position(self, id):
        return self.snakes[id]["head"], self.snakes[id]["body"]
