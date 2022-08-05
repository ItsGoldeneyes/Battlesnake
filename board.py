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
        
        def get_hazards(self):
            return self.hazards
        
        def set_food(self, food):
            self.food = food
            
        def get_food(self):
            return self.food
        
        def get_snakes(self):
            return self.snakes       
        
        def update_snake_collision(self):
            self.snakes_hitbox = []
            for snake in self.snakes.keys():
                self.snakes_hitbox.extend(self.snakes[snake]["body"])
        
        def collision_check(self, move):
            # 1. Check board borders
            if -1 == move["x"] or move["x"] >= self.get_width():
                # print(" -- Horizontal Wall collision")
                return True
            
            if -1 == move["y"] or move["y"] >= self.get_height():
                # print(" -- Vertical Wall collision")
                return True
            
            # 2. Check snakes
            if move in self.get_snake_hitbox():
                # print(" -- Snake collision")
                return True
            
            # 3. Check hazards
            if move in self.board.get_hazards():
                # print(" -- Hazard collision")
                return True
            return False
            
        def move(self, snake_id, move, did_eat = False):
            self.snakes[snake_id]["head"] = move
            self.snakes[snake_id]["body"].insert(0, move)
            if not did_eat:
                self.snakes[snake_id]["body"].pop()
            self.update_snake_collision()
