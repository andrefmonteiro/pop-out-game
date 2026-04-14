import numpy as np
from move import Move

"""
get_winner() → int | None # avaliar resultado
apply_move(move) → Board # devolver Board novo

get_legal_moves() → [Move]
we get a list of Moves and check if the player's move belongs in the list
"""


class Board:

	def get_winner(self) -> int | None:
		# returns 1, 2 or 0 (in case of a tie)
		pass
	
	def get_legal_moves(self) -> list[Move]:
		pass
	
	def apply_move(self, move: Move):
		pass

	def __str__(self):
		# mapping symbols to states for a better print
		symbols = {0: ".", 1: "X", 2: "0"}
		rows = []
		for row in self.grid:
			rows.append(" ".join(symbols[cell] for cell in row))
		return "\n".join(rows)

	def __init__(self):
		# grid with numpy array: 6 height * 7 width - it's indexed by a tuple of ints
		self.current_player = 1
		self.grid = np.zeros((6, 7), np.uint8)


b = Board()
print(b)
