# main_datasets.py
import sys
import os

# Make sure Python finds the 'src' directory
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game.game import Game
from game.player import BotPlayer

def generate_data(n_games=50):
    print(f"Starting data generation ({n_games} games)...")
    for i in range(n_games):
        game = Game()
        game.players = [BotPlayer(), BotPlayer()]

        game.run_silent()

        if (i + 1) % 5 == 0:
            print(f"{i+1} games finished. CSV is growing.")

if __name__ == "__main__":
    generate_data(50)
