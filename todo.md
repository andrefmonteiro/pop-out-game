[] Model Board (src/game/board.py)
	[] drop(col)
	[] pop(col)
	[] get_legal_moves() - uses drop and pop
	[] get_winner()
	[] apply_move(move) - dispatches to drop or pop

[] Model Player (src/game/player.py)
	[] Model subclass HumanPlayer (gets terminal input)
	[] Model subclass BotPlayer (uses mcts function)

[] Model Game (/arc/game/game.py)

[] Model Move (src/game/move.py)
	- drop or pop

[] Implement MCTS function (/src/mcts/mcts.py)
