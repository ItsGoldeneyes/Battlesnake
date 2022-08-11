from snake import BattleSnake
from logic import LogicSnake
from board import Board

import json


board_json = open("resources/tests/food_one.json","r")
board_dict = json.loads(board_json.read())
board = Board(board_dict)
snake = BattleSnake(board)
# print(snake.find_moves(snake.get_head())["up"]['x'])
# board.food_dist(snake.get_head(), snake.find_moves(snake.get_head()))
board.print_board()
print(snake.choose_move())