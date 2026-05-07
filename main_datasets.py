# main_datasets.py
import sys
import os
import time

# Make sure Python finds the 'src' directory
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game.game import Game
from game.player import BotPlayer
from mcts.mcts import MCTSConfig

BEST_CONFIG = MCTSConfig(name="DT-Wide", iterations=200, c=1.414, expansion_count=2)

def generate_data(n_games=50):
    print(f"Starting data generation ({n_games} games, DT-Wide vs DT-Wide)...")
    start = time.perf_counter()
    for i in range(n_games):
        t0 = time.perf_counter()
        game = Game()
        game.players = [BotPlayer(BEST_CONFIG), BotPlayer(BEST_CONFIG)]
        game.run_silent()
        t_game = time.perf_counter() - t0
        t_total = time.perf_counter() - start
        avg = t_total / (i + 1)
        eta = avg * (n_games - i - 1)
        print(f"  Game {i+1}/{n_games} done in {t_game:.1f}s | avg {avg:.1f}s/game | ETA: ~{eta:.0f}s")

if __name__ == "__main__":
    generate_data(1)
