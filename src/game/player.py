"""
subclasses: HumanPlayer, BotPlayer
play_move(Move: player_move)

can we simplify and just have:
- a class BotPlayer whose play_move() calls the mcts function
- a class HumanPlayer whose play_move() gets terminal input

should play_move() be called get_move() instead, as the move only gets played once we check if it's legal with the 
"""


class Player:

    def get_move(self):
        # when HumanPlayer extends this class, we overwrite this method so that we get terminal input
        pass


class HumanPlayer(Player):
	pass