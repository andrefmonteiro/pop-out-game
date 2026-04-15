class Game: # stateless class, only controls the while loop

	def run(self):
		# create player instance
		curr_move = player.get_move()
		self.board = self.board.apply_move(curr_move) # create immutable object, instead of mutating the same Board instance
		# if winner

	def __init__(self):
		pass
	"""
	Game.run() method on a while loop until someone wins
	Player.get_move() -> Board.apply_move() -> Board.get_winner()
	"""
