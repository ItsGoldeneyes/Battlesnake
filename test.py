from src.snake import BattleSnake
from src.logic import LogicSnake
from src.board import Board

import json


board_json = open("resources/tests/floodfill_wall.json","r")
board_dict = json.loads(board_json.read())
board = Board(board_dict)
snake = LogicSnake(board)

board.print_board()
print(snake.choose_move())