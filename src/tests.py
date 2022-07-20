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


class AvoidNeckTest(unittest.TestCase):
    def test_filter_neck_all(self):
        # Arrange
        data = {
            "board": {
                "height": 11,
                "width": 11,
                "food": [
                    {"x": 5, "y": 5},
                    {"x": 9, "y": 0},
                    {"x": 2, "y": 6}],
                "hazards": [{"x": 3, "y": 2}],
                "snakes": [{"id": "snake-508e96ac-94ad-11ea-bb37",
                            "body": [
                                {"x": 0, "y": 0},
                                {"x": 0, "y": 0},
                                {"x": 0, "y": 0}],
                            "head": {"x": 0, "y": 0}},
                           {"id": "snake-b67f4906-94ae-11ea-bb37",
                            "body": [
                                {"x": 5, "y": 4},
                                {"x": 5, "y": 3},
                                {"x": 6, "y": 3},
                                {"x": 6, "y": 2}],
                            "head": {"x": 0, "y": 0}
                            }]},
            "you": {
                "id": "snake-508e96ac-94ad-11ea-bb37",
                "body": [
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 2}],
                "head": {"x": 0, "y": 0}, }}

        logic = MiniMaxSnake()
        logic._parse_board(data)

        # Act
        result = logic._check_loss({"x": 0, "y": 0})

        # Assert
        self.assertEqual(result, False)


if __name__ == "__main__":
    unittest.main()
