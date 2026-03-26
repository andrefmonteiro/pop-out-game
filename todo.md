[] Model Board (src/game/board.py)

[] Model Player (src/game/player.py)
	[] Model subclass HumanPlayer (gets terminal input)
	[] Model subclass BotPlayer (uses mcts function)

[] Model Game (/arc/game/game.py)

[] Model Move (src/game/move.py)
	- drop or pop

[] Implement MCTS function (/src/game/mcts/mcts.py)
	- `def run_mcts(state: Board, n_simulations: int) -> Move`
	- src/game/mcts/mcts.py
