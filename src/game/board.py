import numpy as np

"""
get_winner() → int | None # avaliar resultado
apply_move(move) → Board # devolver Board novo e nao mutar o Board inicial?

option 1:
get_legal_moves() → [Move]
we get a list of Moves and check if the player's move belongs in the list
option 2:
is_move_legal(Move) -> Boolean
pass the player's Move and if it yields True, then we apply the move
"""


class Board:
    def get_winner():
        # returns 1, 2 or 0 (in case of a tie)
        pass

        def apply_move(move: Move):
            # this func gets conditionally called
            pass

    def __init__(self):
        # grid with numpy array: 6 height * 7 width - it's indexed by a tuple of ints
        self.current_player = 1
        self.grid = np.zeros((6, 7), np.uint8)
