"""
Starter Unit Tests using the built-in Python unittest library.
See https://docs.python.org/3/library/unittest.html

You can expand these to cover more cases!

To run the unit tests, use the following command in your terminal,
in the folder where this file exists:

    python src/tests.py -v

"""
import unittest
import json
from board import Board
from snake import BattleSnake


class CollisionTests(unittest.TestCase):
    def test_collision_none(self):
        # Arrange
        board_json = open("resources/tests/collision_none.json","r")
        board_dict = json.loads(board_json.read())
        board_json.close()
        board = Board(board_dict)

        snake = BattleSnake(board)
        potential_moves = snake.find_moves(snake.get_head())
        expected = [False, False, False, False]
        
        # Act
        result = [board.collision_check(move) for move in potential_moves.values()]

        # Assert
        self.assertEqual(result, expected)
    
    def test_collision_up(self):
        # Arrange
        board_json = open("resources/tests/collision_up.json","r")
        board_dict = json.loads(board_json.read())
        board_json.close()
        board = Board(board_dict)

        snake = BattleSnake(board)
        potential_moves = snake.find_moves(snake.get_head())
        expected = [True, False, False, False]
        
        # Act
        result = [board.collision_check(move) for move in potential_moves.values()]

        # Assert
        self.assertEqual(result, expected)
        
    def test_collision_down(self):
        # Arrange
        board_json = open("resources/tests/collision_down.json","r")
        board_dict = json.loads(board_json.read())
        board_json.close()
        board = Board(board_dict)

        snake = BattleSnake(board)
        potential_moves = snake.find_moves(snake.get_head())
        expected = [False, True, False, False]
        
        # Act
        result = [board.collision_check(move) for move in potential_moves.values()]

        # Assert
        self.assertEqual(result, expected)
        
    def test_collision_right(self):
        # Arrange
        board_json = open("resources/tests/collision_right.json","r")
        board_dict = json.loads(board_json.read())
        board_json.close()
        board = Board(board_dict)

        snake = BattleSnake(board)
        potential_moves = snake.find_moves(snake.get_head())
        expected = [False, False, True, False]
        
        # Act
        result = [board.collision_check(move) for move in potential_moves.values()]

        # Assert
        self.assertEqual(result, expected)
        
    def test_collision_left(self):
        # Arrange
        board_json = open("resources/tests/collision_left.json","r")
        board_dict = json.loads(board_json.read())
        board_json.close()
        board = Board(board_dict)

        snake = BattleSnake(board)
        potential_moves = snake.find_moves(snake.get_head())
        expected = [False, False, False, True]
        
        # Act
        result = [board.collision_check(move) for move in potential_moves.values()]

        # Assert
        self.assertEqual(result, expected)

          
if __name__ == "__main__":
    unittest.main()
