"""
Check all next moves (by variable)

give moves percents based on the chance of when enemy wins

give moves percents based on wins

give moves + percent for food based on current percent

assuming your opponent will choose whatever has the lowest score (as this is what’s best for them).

No loop in maxn function just in main

return list of highest probability
"""

import numpy as np

class MaxNSnake:
    def __init__(self, depth=2):
        self.depth = depth
        
    def _parse_board(self, data):
        self.data = data
        self.max_data = data
        self.my_snake = data["you"]
        self.head = self.my_snake["head"]
        self.body = self.my_snake["body"]
        self.board = data["board"]
        self.hazards = data["board"]["hazards"]
        self.food = data["board"]["food"]
        
        self.snakes = self.board['snakes']
        self.snakes_collision = []
        for snake in self.snakes:
            self.snakes_collision.extend(snake["body"])

    def _print_state(self):
        state = ""
        state += f"Snake head: {self.head}\n"
        state += f"Snake body: {self.body}\n"
        state += f"Board: {self.board['width']} x {self.board['height']} \n"
        print(state)

    def _find_moves(self, position):
        return {
            "up": {"x": position['x'], "y": position['y']+1},
            "down": {"x": position['x'], "y": position['y']-1},
            "right": {"x": position['x']+1, "y": position['y']},
            "left": {"x": position['x']-1, "y": position['y']}
        }

    def _collision_check(self, move):
        # print(" -- ", move)
        # 2. Check board borders
        if -1 == move["x"] or move["x"] >= self.board['width']:
            # print(" -- Horizontal Wall collision")
            return True
        if -1 == move["y"] or move["y"] >= self.board['height']:
            # print(" -- Vertical Wall collision")
            return True
        # 3. Check snakes
        if move in self.snakes_collision:
            # print(" -- Snake collision")
            return True
        # 4. Check hazards
        if move in self.hazards:
            # print(" -- Hazard collision")
            return True

        return False
    
    def _position_update(self,snake_num, new_head, did_eat):    
        self.data["board"]["snakes"][snake_num]["head"] = new_head
        self.data["board"]["snakes"][snake_num]["body"].insert(0,new_head)
        if not did_eat:
            self.data["board"]["snakes"][snake_num]["body"].pop()
            
    def maxn(self, snake_num, depth):
        
        if snake_num >= len(self.snakes):
            snake_num = 0 
        
        position = self.snakes[snake_num]["head"]
        snake_id = self.snakes[snake_num]["id"]
        self.data = self.max_data
        max_eval = -np.Infinity
        max_move = {}
        moves = self._find_moves(position)
        
        if depth == 0:
            print("End move:", position)
            eval = 0
            for move in moves.keys():
                if self._collision_check(moves[move]) == False:
                    eval += 1
            return eval
        
        for move in moves.keys():
            print(self._find_moves(position))
            print("move:", move)
            print("move move:",moves[move])
            print("\n")
            if self._collision_check(moves[move]):
                eval = 0
            else:
                eval = self.maxn(snake_num+1, depth-1)
                if max(max_eval, eval):
                    self.max_data = self.data
                    max_move = moves[move]
                    max_eval = max(max_eval, eval)
                    
        self._position_update(snake_num, max_move, False) #eat
        return max_eval


    def choose_move(self, data):
        self._parse_board(data)
        moves = self._find_moves(self.head)

        moveRanks = {}
        for direction in moves.keys():
            # print(direction, moves[direction])
            moveRanks[direction] = self.maxn(0, self.depth)
        print("moveRanks =",moveRanks)
        
        # moveRanks = {move: self.maxn(0, self.depth) for move in moves}
        
        return max(moveRanks, key=moveRanks.get)
             