from snake import BattleSnake
from logic import LogicSnake
from board import Board

import json


board_json = open("resources/tests/collision_none.json","r")
board_dict = json.loads(board_json.read())
board = Board(board_dict)
snake = LogicSnake(board)

board.print_board()
print(snake.choose_move())