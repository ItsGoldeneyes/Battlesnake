import random
from typing import List, Dict
import math


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
        "head": "missile",
        "tail": "rocket",
    }


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_snake = data["you"]      # A dictionary describing your snake's position on the board
    # A dictionary of coordinates like {"x": 0, "y": 0}
    my_head = my_snake["head"]
    # A list of coordinate dictionaries like [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    my_body = my_snake["body"]

    # Uncomment the lines below to see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnake this turn is: {my_snake}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]
    board = data['board']

    possible_moves = _avoid_my_neck(my_body, possible_moves)
    possible_moves = _filter_wall_moves(my_body, possible_moves, board)
    possible_moves = _filter_self_moves(my_body, possible_moves)
    possible_moves = _filter_enemy_moves(my_body, possible_moves, board)

    # if food != {}:
    #     possible_food_moves = []
    #     closest = [food[0]["x"], food[0]["y"]]
    #     for i in food:
    #         if math.dist((my_head["x"], my_head["y"]), (i["x"], i["y"])) < math.dist((my_head["x"], my_head["y"]), (closest["x"], closest["y"])):
    #             closest = [i["x"], i["y"]]

    #     for direction in possible_moves:
    #         if math.dist(moves[direction], closest) > math.dist((my_head["x"], my_head["y"]), closest):
    #             possible_food_moves.append(direction)
    #     if possible_food_moves:
    #         move = random.choice(possible_food_moves)
    #     else:
    #         move = random.choice(possible_moves)
    # else:
    #     move = random.choice(possible_moves)
    if len(possible_moves) == 0:
        move = "up"
    elif len(possible_moves) == 1:
        move = possible_moves[0]
    else:
        move = random.choice(possible_moves)

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move


def _filter_wall_moves(my_body: dict, possible_moves: List[str], board: dict) -> List[str]:
    my_head = my_body[0]
    print("\n")
    board_height = board['height']
    board_width = board['width']

    moves = {
        "up": {"x": my_head['x'], "y": my_head['y']+1},
        "down": {"x": my_head['x'], "y": my_head['y']-1},
        "left": {"x": my_head['x']-1, "y": my_head['y']},
        "right": {"x": my_head['x']+1, "y": my_head['y']}
    }
    print(possible_moves)
    print(moves)
    
    to_remove = []
    
    for direction in possible_moves:
        print(direction)
        # Don't hit walls
        if -1 == moves[direction]["x"] or moves[direction]["x"] == board_width:
            to_remove.append(direction)
        elif -1 == moves[direction]["y"] or moves[direction]["y"] == board_height:
            to_remove.append(direction)
    
    for i in to_remove:
        if i in possible_moves:
            possible_moves.remove(i)
    

    print(possible_moves)
    
    return possible_moves


def _filter_self_moves(my_body: dict, possible_moves: List[str]) -> List[str]:
    my_head = my_body[0]

    moves = {
        "up": {"x": my_head['x'], "y": my_head['y']+1},
        "down": {"x": my_head['x'], "y": my_head['y']-1},
        "left": {"x": my_head['x']-1, "y": my_head['y']},
        "right": {"x": my_head['x']+1, "y": my_head['y']}
    }
    to_remove = []
    for direction in possible_moves:
        for segment in my_body[1:]:
            if segment == moves[direction]:
                to_remove.append(direction)
                
    for i in to_remove:
        if i in possible_moves:
            possible_moves.remove(i)

    return possible_moves


def _filter_enemy_moves(my_body: dict, possible_moves: List[str], board: dict) -> List[str]:
    my_head = my_body[0]

    moves = {
        "up": {"x": my_head['x'], "y": my_head['y']+1},
        "down": {"x": my_head['x'], "y": my_head['y']-1},
        "left": {"x": my_head['x']-1, "y": my_head['y']},
        "right": {"x": my_head['x']+1, "y": my_head['y']}
    }

    other_snakes = board['snakes']
    other_snakes_pos = []
    for snake in other_snakes:
        for i in snake["body"]:
            other_snakes_pos.append({"x": i["x"], "y": i["y"]})

    for direction in possible_moves:
        for segment in other_snakes_pos:
            if segment == moves[direction]:
                possible_moves.remove(direction)

    return possible_moves


def _avoid_my_neck(my_body: dict, possible_moves: List[str]) -> List[str]:
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_head = my_body[0]  # The first body coordinate is always the head
    # The segment of body right after the head is the 'neck'
    my_neck = my_body[1]

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves
