from board import Board
from player import HumanPlayer, BotPlayer

class Game: # stateless class, only controls the while loop

	def run(self):
		self.setup_game_mode()
		curr_player_idx = 0
		is_game_drawable = False
		# we also need to hold state for the board states because of

		while True:
			print(self.board)
			curr_player = self.players[curr_player_idx]
			move = curr_player.get_move(self.board, is_game_drawable) # it's fine to pass this board object reference to the HumanPlayer, as it wont use it
			self.board = self.board.apply_move(move) 
			result = self.board.get_winner() # 1, 2 or draw
			if result:
				break
			else:
				curr_player_idx = 1 - curr_player_idx
		
		if result == 1 or result == 2:
			print(f"Player {curr_player_idx + 1} won!")
		elif result == "draw":
			print("The game is a tie.")




	def __init__(self):
		self.board = Board()
		self.players = []
		self.board_history = []

	def setup_game_mode(self):
		game_mode = input("Human vs Human (1)\nHuman vs Bot (2)\nBot vs Bot (3)\n")
		if game_mode == "1":
			self.players = [HumanPlayer(), HumanPlayer()]
		elif game_mode == "2":
			self.players = [HumanPlayer(), BotPlayer()]
		elif game_mode == "3":
			self.players = [BotPlayer(), BotPlayer()]

	"""
	Game.run() method on a while loop until someone wins
	Player.get_move() -> Board.apply_move() -> Board.get_winner()
	"""
