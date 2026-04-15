from move import Move


"""
subclasses: HumanPlayer, BotPlayer

can we simplify and just have:
- a class BotPlayer whose play_move() calls the mcts function
- a class HumanPlayer whose play_move() gets terminal input
"""


class Player:

    def get_move(self):
        # when HumanPlayer extends this class, we overwrite this method so that we get terminal input
        pass


move_type = input("Drop (D)\nor\nPop(P)\n")
col = input("Column number:\n")


class HumanPlayer(Player):
	# get terminal input
	def get_move(self) -> Move:
		# gets terminal input
		pass

class BotPlayer(Player):
	def get_move(self) -> Move:
		# calls	MCTS
		pass