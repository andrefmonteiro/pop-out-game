"""Round-robin tournament between MCTS variants.

Each variant is an MCTSConfig (different iterations / exploration constant /
expansion width). Every variant plays every other variant in both directions
(A as player 1 vs B as player 2, then B as player 1 vs A as player 2), so for
N variants we run N*(N-1) matchups, each of `games_per_matchup` games. Results
are written to experiments_results.csv at the repo root.

Run:
    python src/experiments/tournament.py
"""

import sys
import os
import csv

# Make the repo's src/ importable when this file is run directly,
# the same trick main_datasets.py uses.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mcts.mcts import MCTSConfig
from game.player import BotPlayer
from game.game import Game


# The four variants we want to compare. To add a new one, just append another
# MCTSConfig -- the round robin and the CSV will grow automatically.
VARIANTS = [
    MCTSConfig(name="Baseline",     iterations=500,  c=1.414, expansion_count=1),
    MCTSConfig(name="DeepThinker",  iterations=2000, c=1.414, expansion_count=1),
    MCTSConfig(name="Explorer",     iterations=500,  c=2.5,   expansion_count=1),
    MCTSConfig(name="WideExpander", iterations=500,  c=1.414, expansion_count=3),
]

# Written at the repo root next to popout_dataset.csv.
RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'experiments_results.csv')


def run_tournament(variants, games_per_matchup=50):
    # Open in 'w' mode so each tournament run starts from a clean file.
    with open(RESULTS_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['bot1_name', 'bot2_name', 'bot1_wins', 'bot2_wins', 'draws', 'total_games'])

        # Ordered round-robin: skip A vs A, but A vs B and B vs A are both run
        # because Pop Out isn't symmetric (player 1 moves first).
        for bot1 in variants:
            for bot2 in variants:
                if bot1 is bot2:
                    continue

                wins, losses, draws = 0, 0, 0
                for i in range(games_per_matchup):
                    # Fresh game + fresh players per game so there's no leaked
                    # state between matches.
                    game = Game()
                    game.players = [BotPlayer(bot1), BotPlayer(bot2)]
                    result = game.run_silent(game_num=i + 1, total_games=games_per_matchup)
                    # run_silent returns Board.get_winner(): 1 / 2 / 0
                    if result == 1:
                        wins += 1
                    elif result == 2:
                        losses += 1
                    else:
                        draws += 1

                writer.writerow([bot1.name, bot2.name, wins, losses, draws, games_per_matchup])
                # Flush so partial results are visible if the run is interrupted.
                f.flush()
                print(f"{bot1.name} vs {bot2.name} -> W:{wins} L:{losses} D:{draws}")

    print("Tournament complete. Results saved to experiments_results.csv")


if __name__ == "__main__":
    run_tournament(VARIANTS)
