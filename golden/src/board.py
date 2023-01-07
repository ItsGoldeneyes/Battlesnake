from snake import BattleSnake
import math
from copy import deepcopy, copy
import json
import os


class Board:
    '''
    This class represents a standard board in a game of BattleSnake
    It contains the attributes of the board (eg. width, height, hazards, food, etc.)
    The snakes in a game are also stored in this object.
    '''
    def __init__(self, data):
        self.data = data
        self.board = data["board"]
        self.turn = self.data["turn"]
        self.gamemode = self.data["game"]["ruleset"]["name"]
        
        self.width = self.board["width"]
        self.height = self.board["height"]
        self.hazards = self.board["hazards"]
        self.food = self.board["food"]
        
        self.self_id = self.data["you"]["id"]
        
        self.snakes = {snake["id"] : BattleSnake(self, snake["id"]) for snake in self.board["snakes"]}
    
    def __deepcopy__(self, memo):
        # id_self = id(self)        # memoization avoids unnecesary recursion
        # _copy = memo.get(id_self)
        # if _copy is None:
        #     _copy = type(self)(
        #         deepcopy(self.data, memo))
        #     memo[id_self] = _copy
        #     _copy.food = deepcopy(self.food)
        #     _copy.hazards = deepcopy(self.hazards)
        #     _copy.snakes = deepcopy(self.snakes)
        # return _copy
        self.update_data()
        # out_file = open("json.json", "w")
        # json.dump(self.data, out_file)
        data = json.loads(json.dumps(self.data))
        return Board(data)
    
    def update_data(self):
        data = self.data
        data['board']['food'] = self.food
        data['snakes'] = []
        for snake_id in self.snakes:
            if snake_id == self.get_self_id():
                data['you'] = self.snakes[snake_id].get_info()
            snake_dict = self.snakes[snake_id].get_info()
            data['snakes'].append(snake_dict)
        
        self.data = data
    
    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_hazards(self):
        return self.hazards
        
    def get_food(self):
        return self.food
    
    def get_turn(self):
        return self.turn
    
    def get_snake(self, snake_id):
        return self.snakes[snake_id]
    
    def get_snakes(self):
        return self.snakes
    
    def get_self_id(self):
        return self.self_id
    
    def get_position(self, id):
        return self.snakes[id].get_body()
    
    def get_health(self, id):
        return self.snakes[id].get_health()
    
    def get_length(self, id):
        return self.snakes[id].get_length()
    
    def point_to_list(self, point):
        return [point["x"],point["y"]]
    
    def get_other_snakes(self, snake_id):
        return {snake.get_id(): snake for snake in self.snakes.values() if snake.id != snake_id}
    
    def wrap_fix(self, move):
        if move["x"] >= self.width-1:
            move["x"] = move["x"] - (self.width-1)
        elif move["x"] < 0:
            move["x"] = move["x"] + (self.width-1)

        if move["y"] >= self.height-1:
            move["y"] = move["y"] - (self.width-1)
        elif move["y"] < 0:
            move["y"] = move["y"] + (self.width-1)

        return move
            
            
    def get_snake_collision(self, id= False):
        snakes_hitbox = []
        for snake_id in self.snakes:
            snakes_hitbox.extend(self.snakes[snake_id].get_body())
        if id:
            if self.snakes[id].get_head() in snakes_hitbox:
                snakes_hitbox.remove(self.snakes[id].get_head())
        return snakes_hitbox
    
    
    def head_collision_check(self, move, snake_id):
        # Get head collisions and check if move is in it
        other_snakes = self.get_other_snakes(snake_id)
        if snake_id:
            heads = [other_snakes[id].get_head() for id in other_snakes.keys() 
                    if other_snakes[id].get_length() >= self.snakes[snake_id].get_length()]
        else:
            heads = [other_snakes[id].get_head() for id in other_snakes.keys()]
        if move in heads:
            return True
        return False
    
    
    def body_collision_check(self, move):
        heads = [self.snakes[id].get_head() for id in self.snakes.keys()]
        bodies = []
        for id in self.snakes.keys():
            bodies.extend(self.snakes[id].get_body())
        # print(move)
        # print("bodies",bodies)
        # print("heads",heads)
        for head in heads:
            if head in bodies:
                bodies.remove(head)
        
        # print(move in bodies)
        if move in bodies:
            return True
        return False
    
    
    def wall_collision_check(self, move):
        # Check for wall collision
        if self.gamemode == "wrapped":
            return False
        
        if -1 == move["x"] or move["x"] >= self.width:
            # print(" -- Horizontal Wall collision")
            return True
        
        if -1 == move["y"] or move["y"] >= self.height:
            # print(" -- Vertical Wall collision")
            return True
        return False


    def hazard_collision_check(self, move):
        # Check for hazard collisions
        if move in self.hazards:
            return True
        return False
    
    def collision_check(self, move, snake_id=False):
        
        if self.head_collision_check(move, snake_id):
            return True
        if self.body_collision_check(move):
            return True
        if self.wall_collision_check(move):
            return True
        if self.hazard_collision_check(move):
            return True
            
        return False
    
    def print_board(self):
        board_array = [[] for i in range(self.height)]
        for y_pos in range(self.height):
            for x_pos in range(self.width):
                coord = {"x": x_pos, "y": y_pos}
                # Check for snakes
                if coord in self.get_snake_collision(False): # Fix with get snake collision
                    board_array[y_pos].append("O")
                # Check for food
                elif coord in self.food:
                    board_array[y_pos].append("F")
                # Check for hazards
                elif coord in self.hazards:
                    board_array[y_pos].append("X")
                
                # Empty space
                else:
                    board_array[y_pos].append("◦")
        board_array.reverse()
        for col in board_array:
            for elem in col:
                print(elem, end=" ")
            print("")
            # print(col)
         
            
    def get_moves(self, position):
        return {
            "up": {"x": position['x'], "y": position['y']+1},
            "down": {"x": position['x'], "y": position['y']-1},
            "left": {"x": position['x']-1, "y": position['y']},
            "right": {"x": position['x']+1, "y": position['y']}
        }
       
       
    def move(self, snake_id, move):
        assert len(move) == 2
        assert type(move) == dict
        
        self.snakes[snake_id].head = move
        self.snakes[snake_id].body.insert(0, move)
        if move not in self.get_food():
            self.snakes[snake_id].body.pop()
    
    
    def has_food(self):
        return not self.food==[]
    
    
    def is_food(self, move):
        return move in self.food


    def point_distance(self, point1, point2):
        return math.sqrt((point1['x']-point2['x'])**2 
                         + (point1['y']-point2['y'])**2)
        

    def food_dist(self, point):
        food = self.get_food()
        food.sort(key = lambda x: self.point_distance(x, point))
        self.food = food
        return self.point_distance(food[0], point)
        
    
    def relative_length(self, snake_id):
        snake_length = self.snakes[snake_id].get_length()
        max_length = 0
        for snake in self.snakes.values():
            if snake.get_id() != snake_id:
                if snake.get_length() > max_length:
                    max_length = snake.get_length()
        # print(snake_length, max_length)
        if snake_length > max_length:
            return 0
        else:
            return max_length
    
    def update_board_after_move(self):
        # self.update_data()
        # Lowers HP, remove dead snakes, remove food
        
        self.snakes = {snake: self.snakes[snake].update(self) for snake in self.snakes}
        new_snakes = deepcopy(self.snakes)
        food_removed = 0
        for snake_id in self.snakes:
            
            if new_snakes[snake_id].get_head() in self.food:
                self.food.remove(new_snakes[snake_id].get_head())
                food_removed += 1
                new_snakes[snake_id].health = 100
        
            if self.collision_check(new_snakes[snake_id].get_head(), snake_id or self.snakes[snake_id].get_health() <= 0):
                for head_snake_id in self.get_other_snakes(snake_id):
                    if self.snakes[head_snake_id].get_head() == self.snakes[snake_id].get_head():
                        if self.snakes[snake_id].get_length() < self.snakes[head_snake_id].get_length():
                            new_snakes.pop(snake_id)
            else:
                new_snakes[snake_id].health = new_snakes[snake_id].get_health() - 1
                
        self.snakes = dict(new_snakes)
        self.food_removed = food_removed
            
            
    def wrap_fix(self, move):
        if move["x"] >= self.width:
            move["x"] = move["x"] - self.width
        elif move["x"] < 0:
            move["x"] = move["x"] + self.width
            
        if move["y"] >= self.height:
            move["y"] = move["y"] - self.height
        elif move["y"] < 0:
            move["y"] = move["y"] + self.height
            
        return move