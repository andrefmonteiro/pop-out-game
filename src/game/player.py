from mcts.mcts import mcts_search
from game.move import Move, MoveType

class Player:
    def get_move(self, board, is_game_drawable):
        pass

class BotPlayer(Player):
    def get_move(self, board, is_game_drawable) -> Move:
        # Increase iterations (e.g. 2000) to make the bot stronger
        return mcts_search(board, iterations=1000)

class HumanPlayer(Player):
    def get_move(self, board, is_game_drawable) -> Move:
        legal = board.get_legal_moves()
        legal_set = {(m.move_type, m.col) for m in legal}
        drops = sorted(m.col for m in legal if m.move_type == MoveType.DROP)
        pops = sorted(m.col for m in legal if m.move_type == MoveType.POP)
        print(f"Legal moves -> DROP cols: {drops}, POP cols: {pops}")
        while True:
            parts = input("Your move (e.g. 'd 3' or 'p 0'): ").strip().lower().split()
            if len(parts) != 2 or parts[0] not in ("d", "p") or not parts[1].lstrip("-").isdigit():
                print("Invalid format. Use '<d|p> <col>', e.g. 'd 3'.")
                continue
            mt = MoveType.DROP if parts[0] == "d" else MoveType.POP
            col = int(parts[1])
            if (mt, col) not in legal_set:
                print("That move is not legal. Try again.")
                continue
            return Move(move_type=mt, col=col)
