"""
Starter Unit Tests using the built-in Python unittest library.
See https://docs.python.org/3/library/unittest.html

You can expand these to cover more cases!

To run the unit tests, use the following command in your terminal,
in the folder where this file exists:

    python src/tests.py -v

"""
import unittest

from minimax import MiniMaxSnake


class CollisionTests(unittest.TestCase):
    def test_filter_none(self):
        # Arrange
        data = {
            "board": {
                "height": 11,
                "width": 11,
                "food": [
                    {"x": 0, "y": 0}],
                "hazards": [{"x": 0, "y": 0}],
                "snakes": [{"id": "snake-b67f4906-94ae-11ea-bb37",
                            "body": [
                                {"x": 0, "y": 0}],
                            "head": {"x": 0, "y": 0}
                            }]},
            "you": {
                "id": "snake-508e96ac-94ad-11ea-bb37",
                "body": [
                    {"x": 0, "y": 0}],
                "head": {"x": 1, "y": 1}, }}

        logic = MiniMaxSnake()
        logic._parse_board(data)

        # Act
        result = logic._collision_check(data["you"]["head"])

        # Assert
        self.assertEqual(result, False)

    def test_filter_body(self):
        # Arrange
        data = {
            "board": {
                "height": 11,
                "width": 11,
                "food": [
                    {"x": 0, "y": 0}],
                "hazards": [{"x": 0, "y": 0}],
                "snakes": [{"id": "snake-b67f4906-94ae-11ea-bb37",
                            "body": [
                                {"x": 0, "y": 0}],
                            "head": {"x": 0, "y": 0}
                            }]},
            "you": {
                "id": "snake-508e96ac-94ad-11ea-bb37",
                "body": [
                    {"x": 1, "y": 1}],
                "head": {"x": 1, "y": 1}, }}

        logic = MiniMaxSnake()
        logic._parse_board(data)

        # Act
        result = logic._collision_check(data["you"]["head"])

        # Assert
        self.assertEqual(result, True)

    def test_filter_snake(self):
        # Arrange
        data = {
            "board": {
                "height": 11,
                "width": 11,
                "food": [
                    {"x": 0, "y": 0}],
                "hazards": [{"x": 0, "y": 0}],
                "snakes": [{"id": "snake-b67f4906-94ae-11ea-bb37",
                            "body": [
                                {"x": 1, "y": 1}],
                            "head": {"x": 0, "y": 0}
                            }]},
            "you": {
                "id": "snake-508e96ac-94ad-11ea-bb37",
                "body": [
                    {"x": 0, "y": 0}],
                "head": {"x": 1, "y": 1}, }}

        logic = MiniMaxSnake()
        logic._parse_board(data)

        # Act
        result = logic._collision_check(data["you"]["head"])

        # Assert
        self.assertEqual(result, True)

    def test_filter_hazards(self):
        # Arrange
        data = {
            "board": {
                "height": 11,
                "width": 11,
                "food": [
                    {"x": 0, "y": 0}],
                "hazards": [{"x": 1, "y": 1}],
                "snakes": [{"id": "snake-b67f4906-94ae-11ea-bb37",
                            "body": [
                                {"x": 0, "y": 0}],
                            "head": {"x": 0, "y": 0}
                            }]},
            "you": {
                "id": "snake-508e96ac-94ad-11ea-bb37",
                "body": [
                    {"x": 0, "y": 0}],
                "head": {"x": 1, "y": 1}, }}

        logic = MiniMaxSnake()
        logic._parse_board(data)

        # Act
        result = logic._collision_check(data["you"]["head"])

        # Assert
        self.assertEqual(result, True)

    def test_filter_wall_up(self):
        # Arrange
        data = {
            "board": {
                "height": 11,
                "width": 11,
                "food": [
                     {"x": 0, "y": 0}],
                "hazards": [{"x": 0, "y": 0}],
                "snakes": [{"id": "snake-b67f4906-94ae-11ea-bb37",
                            "body": [
                                {"x": 0, "y": 0}],
                            "head": {"x": 0, "y": 0}
                            }]},
            "you": {
                "id": "snake-508e96ac-94ad-11ea-bb37",
                "body": [
                    {"x": 0, "y": 0}],
                "head": {"x": 1, "y": 11}, }}

        logic = MiniMaxSnake()
        logic._parse_board(data)

        # Act
        result = logic._collision_check(data["you"]["head"])

        # Assert
        self.assertEqual(result, True)

    def test_filter_wall_down(self):
        # Arrange
        data = {
            "board": {
                "height": 11,
                "width": 11,
                "food": [
                     {"x": 0, "y": 0}],
                "hazards": [{"x": 0, "y": 0}],
                "snakes": [{"id": "snake-b67f4906-94ae-11ea-bb37",
                            "body": [
                                {"x": 0, "y": 0}],
                            "head": {"x": 0, "y": 0}
                            }]},
            "you": {
                "id": "snake-508e96ac-94ad-11ea-bb37",
                "body": [
                    {"x": 0, "y": 0}],
                "head": {"x": 1, "y": -1}, }}

        logic = MiniMaxSnake()
        logic._parse_board(data)

        # Act
        result = logic._collision_check(data["you"]["head"])

        # Assert
        self.assertEqual(result, True)

    def test_filter_wall_left(self):
        # Arrange
        data = {
            "board": {
                "height": 11,
                "width": 11,
                "food": [
                     {"x": 0, "y": 0}],
                "hazards": [{"x": 0, "y": 0}],
                "snakes": [{"id": "snake-b67f4906-94ae-11ea-bb37",
                            "body": [
                                {"x": 0, "y": 0}],
                            "head": {"x": 0, "y": 0}
                            }]},
            "you": {
                "id": "snake-508e96ac-94ad-11ea-bb37",
                "body": [
                    {"x": 0, "y": 0}],
                "head": {"x": -1, "y": 1}, }}

        logic = MiniMaxSnake()
        logic._parse_board(data)

        # Act
        result = logic._collision_check(data["you"]["head"])

        # Assert
        self.assertEqual(result, True)

    def test_filter_wall_right(self):
        # Arrange
        data = {
            "board": {
                "height": 11,
                "width": 11,
                "food": [
                     {"x": 0, "y": 0}],
                "hazards": [{"x": 0, "y": 0}],
                "snakes": [{"id": "snake-b67f4906-94ae-11ea-bb37",
                            "body": [
                                {"x": 0, "y": 0}],
                            "head": {"x": 0, "y": 0}
                            }]},
            "you": {
                "id": "snake-508e96ac-94ad-11ea-bb37",
                "body": [
                    {"x": 0, "y": 0}],
                "head": {"x": 11, "y": 1}, }}

        logic = MiniMaxSnake()
        logic._parse_board(data)

        # Act
        result = logic._collision_check(data["you"]["head"])

        # Assert
        self.assertEqual(result, True)


class FindMovesTests(unittest.TestCase):
    def test_find_moves(self):
        # Arrange
        move = {"x": 1, "y": 1}
        correct = {
            "up": {"x": 1, "y": 2},
            "down": {"x": 1, "y": 0},
            "right": {"x": 2, "y": 1},
            "left": {"x": 0, "y": 1}
        }
        logic = MiniMaxSnake()

        # Act
        result = logic._find_moves(move)

        # Assert
        self.assertEqual(result, correct)


if __name__ == "__main__":
    unittest.main()
