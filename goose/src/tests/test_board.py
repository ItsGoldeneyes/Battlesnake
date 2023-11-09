from copy import deepcopy
import funcs.board
import unittest

class TestBoard(unittest.TestCase):
    
    def setUp(self):
        self.board = {
            'height': 10,
            'width': 10,
            'food': [(3, 4), (7, 8)],
            'hazard': [(2, 2), (8, 8)],
            'hazard_damage': 10,
            'snakes': {
                'snake1': {
                    'id': 'snake1',
                    'name': 'Snake 1',
                    'health': 100,
                    'body': [(5, 5), (5, 6), (5, 7)],
                    'head': (5, 5),
                    'length': 3,
                    'shout': ''
                },
                'snake2': {
                    'id': 'snake2',
                    'name': 'Snake 2',
                    'health': 100,
                    'body': [(3, 3), (3, 4), (3, 5)],
                    'head': (3, 3),
                    'length': 3,
                    'shout': ''
                }
            }
        }
    
    def test_make_move(self):
        # Test that make_move returns a new board with the snake moved in the specified direction
        new_board = make_move(self.board, 'snake1', 'right')
        self.assertNotEqual(new_board, self.board)
        self.assertEqual(new_board['snakes']['snake1']['body'], [(5, 6), (5, 7), (5, 8)])
        
        # Test that make_move raises an exception if the move is invalid
        with self.assertRaises(ValueError):
            make_move(self.board, 'snake1', 'up')
    
    def test_unmake_move(self):
        # Test that unmake_move restores the board to its previous state
        old_board = deepcopy(self.board)
        state = make_move(self.board, 'snake1', 'right')
        unmake_move(self.board, 'snake1', state)
        self.assertEqual(self.board, old_board)
    
    def test_food_check(self):
        # Test that food_check returns True if the snake is on a food item
        snake = self.board['snakes']['snake1']
        self.assertTrue(food_check(self.board, snake))
        
        # Test that food_check returns False if the snake is not on a food item
        snake = self.board['snakes']['snake2']
        self.assertFalse(food_check(self.board, snake))
    
    def test_collision_check(self):
        # Test that collision_check returns 0 if there are no collisions
        snake = self.board['snakes']['snake1']
        self.assertEqual(collision_check(self.board, snake), 0)
        
        # Test that collision_check returns 1 if the snake collides with a wall
        self.board['snakes']['snake1']['body'] = [(0, 5), (0, 6), (0, 7)]
        snake = self.board['snakes']['snake1']
        self.assertEqual(collision_check(self.board, snake), 1)
        
        # Test that collision_check returns 2 if the snake collides with itself
        self.board['snakes']['snake1']['body'] = [(5, 5), (5, 6), (5, 7), (4, 7), (4, 6), (4, 5)]
        snake = self.board['snakes']['snake1']
        self.assertEqual(collision_check(self.board, snake), 2)
        
        # Test that collision_check returns 3 if the snake collides with another snake
        self.board['snakes']['snake2']['body'] = [(5, 5), (5, 6), (5, 7)]
        snake = self.board['snakes']['snake1']
        self.assertEqual(collision_check(self.board, snake), 3)
import unittest
from funcs.board import make_move, unmake_move, food_check, collision_check
