# main_datasets.py
import sys
import os

# Garante que o Python encontra a pasta 'src'
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game.game import Game
from game.player import BotPlayer

def gerar_dados(n_jogos=50):
    print(f"🚀 A iniciar a geração de dados ({n_jogos} jogos)...")
    for i in range(n_jogos):
        game = Game()
        # Removidos os argumentos color=1 e color=2
        game.players = [BotPlayer(), BotPlayer()] 
        
        # Este método tem de estar dentro da classe Game no ficheiro game.py
        game.run_silencioso() 
        
        if (i + 1) % 5 == 0:
            print(f"✅ {i+1} jogos terminados. O CSV está a crescer!")

if __name__ == "__main__":
    gerar_dados(50)