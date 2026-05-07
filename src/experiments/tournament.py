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
import time

# Make the repo's src/ importable when this file is run directly,
# the same trick main_datasets.py uses.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mcts.mcts import MCTSConfig
from game.player import BotPlayer
from game.game import Game


# The four variants we want to compare. To add a new one, just append another
# MCTSConfig -- the round robin and the CSV will grow automatically.
#
# Iterations were reduced from the original spec (500/2000/500/500) because at
# those values a full 50-game tournament took ~40h on this machine. The 4x
# ratio between Baseline and DeepThinker is preserved so the comparison still
# means roughly the same thing; if Board.apply_move is later optimized to
# avoid copy.deepcopy, we can raise these numbers back up.
# Pilot (2026-05-07): avg 6.7s/game → 100 games/matchup ≈ 2h 14min total.
VARIANTS = [
    MCTSConfig(name="Baseline",     iterations=50,  c=1.414, expansion_count=1),
    MCTSConfig(name="DeepThinker",  iterations=200, c=1.414, expansion_count=1),
    MCTSConfig(name="Explorer",     iterations=50,  c=2.5,   expansion_count=1),
    MCTSConfig(name="WideExpander", iterations=50,  c=1.414, expansion_count=3),
]

# Toy versions of VARIANTS used to verify the wiring in seconds rather than
# hours. Keep the iteration counts very small -- the goal here is "do all the
# pieces (tournament loop, progress prints, CSV writing) work?", not "is one
# variant stronger than another?". Use SMOKE_VARIANTS with a small
# games_per_matchup before committing to the real VARIANTS run.
SMOKE_VARIANTS = [
    MCTSConfig(name="Baseline",     iterations=10, c=1.414, expansion_count=1),
    MCTSConfig(name="DeepThinker",  iterations=20, c=1.414, expansion_count=1),
    MCTSConfig(name="Explorer",     iterations=10, c=2.5,   expansion_count=1),
    MCTSConfig(name="WideExpander", iterations=10, c=1.414, expansion_count=3),
]

# Written at the repo root next to popout_dataset.csv.
RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'experiments_results.csv')


def _save_csv(tally, games_played_per_matchup):
    # Overwrite the file with current standings -- always exactly one row per
    # matchup. Called after every round so a crash loses at most one round.
    with open(RESULTS_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['bot1_name', 'bot2_name', 'bot1_wins', 'bot2_wins', 'draws', 'total_games'])
        for (n1, n2), (w, l, d) in tally.items():
            writer.writerow([n1, n2, w, l, d, games_played_per_matchup])


def run_tournament(variants, games_per_matchup=50):
    # Build the ordered matchup list once.
    # A vs B and B vs A are separate because Pop Out isn't symmetric.
    matchups = [
        (bot1, bot2)
        for bot1 in variants
        for bot2 in variants
        if bot1 is not bot2
    ]
    total_games_all = len(matchups) * games_per_matchup
    games_done = 0
    tournament_start = time.perf_counter()

    # Running tally per matchup: [wins, losses, draws].
    tally = {(b1.name, b2.name): [0, 0, 0] for b1, b2 in matchups}

    # Interleaved loop: play one game of every matchup (a "round"), then
    # repeat. After each round the CSV is overwritten with current standings.
    # If the run crashes, every matchup has the same number of games --
    # the snapshot is always representative.
    for round_i in range(games_per_matchup):
        for bot1, bot2 in matchups:
            game = Game()
            game.players = [BotPlayer(bot1), BotPlayer(bot2)]

            t0 = time.perf_counter()
            result = game.run_silent(game_num=round_i + 1, total_games=games_per_matchup)
            t_game = time.perf_counter() - t0

            key = (bot1.name, bot2.name)
            if result == 1:
                tally[key][0] += 1
            elif result == 2:
                tally[key][1] += 1
            else:
                tally[key][2] += 1

            games_done += 1
            t_total = time.perf_counter() - tournament_start
            avg = t_total / games_done
            eta = avg * (total_games_all - games_done)
            print(f"  → done in {t_game:.1f}s | avg {avg:.1f}s/game | "
                  f"{games_done}/{total_games_all} games | ETA: ~{eta:.0f}s")

        # Persist after every round and print a summary block.
        _save_csv(tally, round_i + 1)
        print("#" * 20)
        print(f"Round {round_i + 1}/{games_per_matchup} complete — current standings:")
        for (n1, n2), (w, l, d) in tally.items():
            print(f"  {n1} vs {n2}  W:{w} L:{l} D:{d}")
        print("#" * 20)

    t_total = time.perf_counter() - tournament_start
    avg = t_total / total_games_all
    projection = avg * 1200  # projection for 100 games/matchup (useful during pilots)
    proj_h = int(projection // 3600)
    proj_m = int((projection % 3600) // 60)
    print(f"\nTournament complete. Results saved to experiments_results.csv")
    print(f"Total time: {t_total:.0f}s | Average per game: {avg:.1f}s")
    print(f"→ For 100 games/matchup (1200 total): estimate {projection:.0f}s (~{proj_h}h {proj_m}m)")


if __name__ == "__main__":
    # Real tournament: 100 games/matchup, ~2h 14min expected.
    # Pilot confirmed avg 6.7s/game with these variants on 2026-05-07.
    run_tournament(VARIANTS, games_per_matchup=100)
