# from snake import BattleSnake
# from logic import LogicSnake
# from board import Board

# import json



# food = {"x":1, "y":3}

# move1 = {"x":2, "y":3}
# move2 = {"x":5, "y":3}

# dist = abs((food["x"]+food["y"]) - (move2["x"]+move2["y"]))
# print(dist)



food_dists = {
            "up": 2,
            "down": 4,
            "right": 5,
            "left": 1
        }

print(max(food_dists, key=food_dists.get))