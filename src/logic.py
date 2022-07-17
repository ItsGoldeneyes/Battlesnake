import random
from typing import List, Dict
import math


class SnakeLogic:
    def __init__(self, look_ahead=2):
        self.look_ahead = look_ahead
        self.data = None
        self.head = None
        self.good_moves = None
        self.potential_moves = None

    def get_info() -> dict:
        """
        This controls your Battlesnake appearance and author permissions.
        For customization options, see https://docs.battlesnake.com/references/personalization

        TIP: If you open your Battlesnake URL in browser you should see this data.
        """
        return {
            "apiversion": "1",
            "author": "Goldeneyes",
            "color": "#EB6443",  # "color": "#EB6443",
            "self.head": "missile",
            "tail": "rocket",
        }

    def choose_move(self, data: dict) -> str:
        """
        data: Dictionary of all Game Board data as received from the Battlesnake Engine.
        For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

        return: A String, the single move to make. One of "up", "down", "left" or "right".

        Use the information in 'data' to decide your next move. The 'data' variable can be interacted
        with as a Python Dictionary, and contains all of the information about the Battlesnake board
        for each move of the game.

        """

        my_snake = data["you"]
        head = my_snake["head"]
        body = my_snake["body"]
        good_moves = ["up", "down", "left", "right"]
        board = data['board']

        self.set_state(board, head, body, good_moves, my_snake)

        self.good_moves = self._filter_my_neck()
        self.good_moves = self._filter_wall_moves()
        self.good_moves = self._filter_self_moves()
        self.good_moves = self._filter_enemy_moves()

        # if food != {}:
        #     possible_food_moves = []
        #     closest = [food[0]["x"], food[0]["y"]]
        #     for i in food:
        #         if math.dist((self.head["x"], self.head["y"]), (i["x"], i["y"])) < math.dist((self.head["x"], self.head["y"]), (closest["x"], closest["y"])):
        #             closest = [i["x"], i["y"]]

        #     for direction in good_moves:
        #         if math.dist(moves[direction], closest) > math.dist((self.head["x"], self.head["y"]), closest):
        #             possible_food_moves.append(direction)
        #     if possible_food_moves:
        #         move = random.choice(possible_food_moves)
        #     else:
        #         move = random.choice(good_moves)
        # else:
        #     move = random.choice(good_moves)

        if len(self.good_moves) == 0:
            move = "up"
        elif len(self.good_moves) == 1:
            move = self.good_moves[0]
        else:
            move = random.choice(self.good_moves)

        print(
            f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {self.good_moves}")

        return move

    def set_state(self, board: dict, head: dict, body: list, good_moves: dict, my_snake: dict, ):
        self.my_snake = my_snake
        self.head = head
        self.body = body
        self.good_moves = good_moves
        self.board = board
        
        self.potential_moves = {
        "up": {"x": self.head['x'], "y": self.head['y']+1}, 
        "down": {"x": self.head['x'], "y": self.head['y']-1},
        "right": {"x": self.head['x']+1, "y": self.head['y']},
        "left": {"x": self.head['x']-1, "y": self.head['y']}
        }

        # Find a better way to do this
        other_snakes_dict = self.board['snakes']
        self.other_snakes = []
        for snake in other_snakes_dict:
            for i in snake["body"]:
                self.other_snakes.append({"x": i["x"], "y": i["y"]})
                
                
        self.state = ""
        
        self.state += f"Snake head: {self.head}\n"
        self.state += f"Snake body: {self.body}\n"
        self.state += f"Board: {self.board['width']} x {self.board['height']} \n"

    def _filter_wall_moves(self) -> List[str]:
        board_height = self.board['height']
        board_width = self.board['width']

        to_remove = []
        
        for direction in self.good_moves:
            
            # Don't hit walls
            if -1 == self.potential_moves[direction]["x"] or self.potential_moves[direction]["x"] == board_width:
                to_remove.append(direction)
            elif -1 == self.potential_moves[direction]["y"] or self.potential_moves[direction]["y"] == board_height:
                to_remove.append(direction)

        for i in to_remove:
            if i in self.good_moves:
                self.good_moves.remove(i)

        return self.good_moves  # For testing purposes

    def _filter_self_moves(self):
        """
        USES - body, moves, board
        
        
        """

        to_remove = []
        for direction in self.good_moves:
            for segment in self.body[1:]:
                if segment == self.potential_moves[direction]:
                    to_remove.append(direction)

        for i in to_remove:
            if i in self.good_moves:
                self.good_moves.remove(i)

        return self.good_moves  # For testing purposes

    def _filter_enemy_moves(self) -> List[str]:
        """
        USES - body, moves, board
        
        
        """
        for direction in self.good_moves:
            for segment in self.other_snakes:
                if segment == self.potential_moves[direction]:
                    self.good_moves.remove(direction)

        return self.good_moves  # For testing purposes

    def _filter_my_neck(self) -> List[str]:
        """
        body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
                e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
        good_moves: List of strings. Moves to pick from.
                e.g. ["up", "down", "left", "right"]

        return: The list of remaining good_moves, with the 'neck' direction removed
        """

        # The segment of body right after the self.head is the 'neck'
        my_neck = self.body[1]

        if my_neck["x"] < self.head["x"]:  # my neck is left of my self.head
            self.good_moves.remove("left")
        elif my_neck["x"] > self.head["x"]:  # my neck is right of my self.head
            self.good_moves.remove("right")
        elif my_neck["y"] < self.head["y"]:  # my neck is below my self.head
            self.good_moves.remove("down")
        elif my_neck["y"] > self.head["y"]:  # my neck is above my self.head
            self.good_moves.remove("up")

        return self.good_moves  # For testing purposes
