"""Visualization for MCTS tournament results.

Reads experiments_results.csv and produces:
  - src/experiments/graphs/heatmap.png  : win-rate matrix (row bot vs column bot)
  - src/experiments/graphs/barchart.png : overall win rate per variant

Run from the repo root:
    python src/experiments/visualize.py
"""

import sys
import os

# Same sys.path trick as tournament.py so this runs as a standalone script.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# All plots land here so they stay out of the repo root.
GRAPHS_DIR = os.path.join(os.path.dirname(__file__), 'graphs')


def load_results(filepath: str) -> pd.DataFrame:
    """Load experiments_results.csv into a DataFrame."""
    return pd.read_csv(filepath)


def plot_win_rate_heatmap(df: pd.DataFrame, output_path: str = None) -> None:
    """
    Generate a win rate heatmap matrix where cell (A, B) shows
    the win rate of bot A against bot B. Save to output_path.
    """
    if output_path is None:
        output_path = os.path.join(GRAPHS_DIR, 'heatmap.png')

    # Compute win rate for each (bot1, bot2) pair.
    # Cells on the diagonal don't exist (no self-play) and stay NaN.
    data = df.copy()
    data['win_rate'] = data['bot1_wins'] / data['total_games']
    pivot = data.pivot(index='bot1_name', columns='bot2_name', values='win_rate')

    _, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        pivot,
        annot=True,       # print the number inside each cell
        fmt='.2f',        # two decimal places
        cmap='RdYlGn',    # red = bot loses, green = bot wins
        vmin=0, vmax=1,
        linewidths=0.5,
        ax=ax,
    )
    ax.set_title('Win rate: row bot (player 1) vs column bot (player 2)')
    ax.set_xlabel('Opponent (bot2)')
    ax.set_ylabel('Challenger (bot1)')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f'Heatmap saved to {output_path}')


def plot_win_rate_barchart(df: pd.DataFrame, output_path: str = None) -> None:
    """
    Generate a bar chart showing the overall win rate of each variant
    across all matchups combined. Save to output_path.
    """
    if output_path is None:
        output_path = os.path.join(GRAPHS_DIR, 'barchart.png')

    # For each variant (as player 1), total wins / total games played.
    agg = (
        df.groupby('bot1_name')
        .agg(total_wins=('bot1_wins', 'sum'), total_played=('total_games', 'sum'))
        .reset_index()
    )
    agg['win_rate'] = agg['total_wins'] / agg['total_played']
    agg = agg.sort_values('win_rate', ascending=False)

    _, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(agg['bot1_name'], agg['win_rate'], color='steelblue', edgecolor='white')

    # Label each bar with the exact win rate.
    for bar, rate in zip(bars, agg['win_rate']):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.02,
            f'{rate:.2f}',
            ha='center', va='bottom', fontsize=10,
        )

    ax.set_ylim(0, 1.15)
    ax.set_ylabel('Win rate (as player 1)')
    ax.set_title('Overall win rate per MCTS variant')
    # Dotted line at 50% so it's easy to see who beats random chance.
    ax.axhline(0.5, color='gray', linestyle='--', linewidth=1, label='50%')
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f'Bar chart saved to {output_path}')


def generate_all(results_path: str = "first_tournament_results.csv") -> None:
    """Load results and generate all plots."""
    df = load_results(results_path)
    plot_win_rate_heatmap(df)
    plot_win_rate_barchart(df)


if __name__ == "__main__":
    generate_all()
