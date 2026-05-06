from mcts.mcts import mcts_search, MCTSConfig
from game.move import Move, MoveType

class Player:
    def get_move(self, board, is_game_drawable):
        pass

class BotPlayer(Player):
    def __init__(self, config: MCTSConfig | None = None):
        # Default config keeps existing call sites (BotPlayer()) working;
        # the tournament passes a specific MCTSConfig per variant.
        self.config = config if config is not None else MCTSConfig()

    def get_move(self, board, is_game_drawable) -> Move:
        return mcts_search(board, self.config)

class HumanPlayer(Player):
    def get_move(self, board, is_game_drawable) -> Move:
        legal = board.get_legal_moves()
        legal_set = {(m.move_type, m.col) for m in legal}
        drops = sorted(m.col + 1 for m in legal if m.move_type == MoveType.DROP)
        pops = sorted(m.col + 1 for m in legal if m.move_type == MoveType.POP)
        print(f"Legal moves -> DROP cols: {drops}, POP cols: {pops}")
        while True:
            parts = input("Your move (e.g. 'd 3' or 'p 1'): ").strip().lower().split()
            if len(parts) != 2 or parts[0] not in ("d", "p") or not parts[1].isdigit():
                print("Invalid format. Use '<d|p> <col>', e.g. 'd 3'.")
                continue
            mt = MoveType.DROP if parts[0] == "d" else MoveType.POP
            col = int(parts[1]) - 1
            if (mt, col) not in legal_set:
                print("That move is not legal. Try again.")
                continue
            return Move(move_type=mt, col=col)
