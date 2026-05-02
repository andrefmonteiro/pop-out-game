from game.board import Board
from game.player import HumanPlayer, BotPlayer

class Game:
    def __init__(self):
        self.board = Board()
        self.players = []

    def setup_game_mode(self):
        print("1. Human vs Human\n2. Human vs Bot\n3. Bot vs Bot")
        mode = input("Escolha o modo: ")
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
            print(self.board)
            move = self.players[curr_idx].get_move(self.board, False)
            self.board = self.board.apply_move(move)
            
            winner = self.board.get_winner()
            if winner is not None:
                print(self.board)
                if winner == 0: print("Empate!")
                else: print(f"Jogador {winner} venceu!")
                break
            curr_idx = 1 - curr_idx

    def run_silencioso(self):
        """Versão do loop de jogo sem prints para gerar dados rapidamente."""
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