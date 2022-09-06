from board import Board
from floodfill_board import floodfill

import json


board_json = open("resources/tests/floodfill_wall.json","r")
board_dict = json.loads(board_json.read())
board = Board(board_dict)
snake_id = board.get_self_id()
potential_moves = board.find_moves(board.get_position(snake_id)[0])
# print(snake.find_moves(snake.get_head())["up"]['x'])
# board.food_dist(snake.get_head(), snake.find_moves(snake.get_head()))
for move in potential_moves:
    ff = floodfill()
    flood_score = ff.floodfill(board, potential_moves[move], snake_id)
    print(ff.accessed)
    print(flood_score)
    board.print_board()

# flood_scores = {move: ff.floodfill(board= board, move= potential_moves[move], snake_id= snake_id) for move in potential_moves}
