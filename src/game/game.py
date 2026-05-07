from game.board import Board
from game.player import HumanPlayer, BotPlayer

class Game:
    def __init__(self):
        self.board = Board()
        self.players = []

    def setup_game_mode(self):
        print("1. Human vs Human\n2. Human vs Bot\n3. Bot vs Bot")
        mode = input("Choose mode: ")
        if mode == "1":
            self.players = [HumanPlayer(), HumanPlayer()]
        elif mode == "2":
            self.players = [HumanPlayer(), BotPlayer()]
        else:
            self.players = [BotPlayer(), BotPlayer()]

    def run(self):
        self.setup_game_mode()
        curr_idx = 0

        while True:
            print("\n" + "=" * 30)
            print(f"Player {self.board.current_player}'s turn")
            print(self.board)
            move = self.players[curr_idx].get_move(self.board, False)
            self.board = self.board.apply_move(move)

            winner = self.board.get_winner()
            if winner is not None:
                print("\n" + "=" * 30)
                print(self.board)
                if winner == 0: print("Draw!")
                else: print(f"Player {winner} wins!")
                break
            curr_idx = 1 - curr_idx

    def run_silent(self, game_num: int = None, total_games: int = None):
        """Game loop without prints, for fast dataset generation / tournaments.

        When called with both game_num and total_games, prints a single
        progress line at the start so a long-running tournament shows life.
        Bot names come from each BotPlayer's MCTSConfig; humans show as 'Human'.
        """
        if game_num is not None and total_games is not None:
            def _name(p):
                # BotPlayer carries a config with a .name; HumanPlayer doesn't.
                return p.config.name if isinstance(p, BotPlayer) else "Human"
            p1, p2 = self.players[0], self.players[1]
            print(f"[{_name(p1)} vs {_name(p2)}] Game {game_num}/{total_games}")

        curr_player_idx = 0
        while True:
            curr_player = self.players[curr_player_idx]
            move = curr_player.get_move(self.board, False)
            self.board = self.board.apply_move(move)

            result = self.board.get_winner()
            if result is not None:
                break
            curr_player_idx = 1 - curr_player_idx
        return result
