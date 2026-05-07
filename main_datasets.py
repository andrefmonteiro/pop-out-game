# main_datasets.py
import sys
import os
import csv
import time

# Make sure Python finds the 'src' directory
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game.game import Game
from game.player import BotPlayer
from mcts.mcts import MCTSConfig, set_game_id

BEST_CONFIG = MCTSConfig(name="DT-Wide", iterations=200, c=1.414, expansion_count=2)

def _last_game_id() -> int:
    """Return the highest game_id already in the CSV, or 0 if the file doesn't exist."""
    if not os.path.exists('popout_dataset.csv'):
        return 0
    with open('popout_dataset.csv', newline='') as f:
        last = 0
        for row in csv.DictReader(f):
            last = int(row['game_id'])
        return last

def generate_data(n_games=50):
    start_id = _last_game_id() + 1
    end_id = start_id + n_games - 1
    print(f"Starting data generation ({n_games} games, DT-Wide vs DT-Wide, game IDs {start_id}–{end_id})...")
    start = time.perf_counter()
    for i in range(n_games):
        set_game_id(start_id + i)
        t0 = time.perf_counter()
        game = Game()
        game.players = [BotPlayer(BEST_CONFIG), BotPlayer(BEST_CONFIG)]
        game.run_silent()
        t_game = time.perf_counter() - t0
        t_total = time.perf_counter() - start
        avg = t_total / (i + 1)
        eta = avg * (n_games - i - 1)
        print(f"  Game {start_id + i}/{end_id} done in {t_game:.1f}s | avg {avg:.1f}s/game | ETA: ~{eta:.0f}s")

if __name__ == "__main__":
    generate_data(100)