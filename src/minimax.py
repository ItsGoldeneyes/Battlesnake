"""
Check all next moves (by variable)

give moves percents based on the chance of when enemy wins

give moves percents based on wins

give moves + percent for food based on current percent

assuming your opponent will choose whatever has the lowest score (as this is what’s best for them).

No loop in minimax function just in main

return list of highest probability
"""


def _score_moves(moves, potential_moves):
        directions = potential_moves.keys()
        final_moves = {}
        
        for direction in directions:
            if direction in moves: 
                final_moves[direction] = 1
            else:
                final_moves[direction] = 0
        
        return final_moves