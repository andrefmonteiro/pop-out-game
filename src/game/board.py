import numpy as np

"""
get_legal_moves() → [Move] # ou ver se apply_move é legal?
apply_move(move) → Board # devolver Board novo e nao mutar o Board inicial?
get_winner() → int | None # avaliar resultado
"""


class Board:
    def get_winner():
        pass

    def __init__(self):
        # grid with numpy array: 6 height * 7 width - it's indexed by a tuple of ints
        self.current_player = 1
        self.grid = np.zeros((6, 7), np.uint8)


my_board = Board()
print(my_board.grid)
