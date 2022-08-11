from snake import BattleSnake
from logic import LogicSnake
from board import Board

import json


board_json = open("resources/tests/floodfill_wall.json","r")
board_dict = json.loads(board_json.read())
board = Board(board_dict)
snake = LogicSnake(board)
# print(snake.find_moves(snake.get_head())["up"]['x'])
# board.food_dist(snake.get_head(), snake.find_moves(snake.get_head()))
potential_moves = snake.find_moves(snake.get_head())

flood_scores = {move:snake.flood_fill(snake.board, potential_moves[move], []) for move in potential_moves}
print(len(set(flood_scores.values())))
print(flood_scores)
board.print_board()
print(snake.choose_move())