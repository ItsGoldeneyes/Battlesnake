"""
Check all next moves (by variable)

give moves percents based on the chance of when enemy wins

give moves percents based on wins

give moves + percent for food based on current percent

assuming your opponent will choose whatever has the lowest score (as this is what’s best for them).

No loop in minimax function just in main

return list of highest probability
"""

import numpy as np

class MiniMaxSnake:
    def __init__(self, depth=3):
        self.depth = depth
        
    def _parse_board(self, data):
        self.my_snake = data["you"]
        self.head = self.my_snake["head"]
        self.body = self.my_snake["body"]
        self.board = data['board']
        self.hazards = data["board"]["hazards"]
        
        snakes_dict = self.board['snakes']
        self.snakes = []
        for snake in snakes_dict:
            if snake["id"] != self.my_snake["id"]:
                self.snakes.append(snake["body"])
                    
         # Food           
                    
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

    def  _check_loss(self, move):
        # 1. Check for self
        if move in self.body:
            return True
        # 2. Check board borders
        if -1 == move["x"] or move["x"] == self.board['width']:
            return True
        if -1 == move["y"] or move["y"] == self.board['height']:
            return True
        # 3. Check snakes
        if move in self.snakes:
            return True
        # 4. Check hazards
        if move in self.hazards:
            return True
        
        return False

    def minimax(self, position, depth, alpha, beta, isMaximizing):
        # total = 0
        if self._check_loss(position):
            return 0
        # if _check_food(position):
        #     total += 2
        # if _check_kill(position):
        #   total += 3
        if depth == 0:
            return 1
        
        if isMaximizing:
            maxEval = -np.Infinity
            moves = self._find_moves(position)
            for move in moves.keys():
                eval = self.minimax(moves[move], depth-1, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = np.Infinity
            moves = self._find_moves(position)
            for move in moves.keys():
                eval = self.minimax(moves[move], depth-1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return minEval
                        
    def choose_move(self, data):
        self._parse_board(data)
        moves = self._find_moves(self.head)
        
        moveRanks = {}
        for move in moves.keys():
            moveRanks[move] = self.minimax(moves[move], self.depth, -np.Infinity, np.Infinity, True)
        print(moveRanks)
        return max(moveRanks, key=moveRanks.get)
             