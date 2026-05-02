from mcts.mcts import mcts_search
from game.move import Move, MoveType

class Player:
    def get_move(self, board, is_game_drawable):
        pass

class BotPlayer(Player):
    def get_move(self, board, is_game_drawable) -> Move:
        # Podes aumentar as iterações (ex: 2000) para o bot ser mais forte[cite: 1]
        return mcts_search(board, iterations=1000)

class HumanPlayer(Player):
    def get_move(self, board, is_game_drawable) -> Move:
        # Implementação para ler do terminal (D/P e Coluna)
        pass