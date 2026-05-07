"""Visualization scaffolding for the MCTS tournament results.

Implementations will be added later -- this module currently only declares
the function surface so other code can import the names without breakage.
"""

# Implementations will be added later.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_results(filepath: str) -> pd.DataFrame:
    """Load experiments_results.csv into a DataFrame."""
    pass


def plot_win_rate_heatmap(df: pd.DataFrame, output_path: str = "heatmap.png") -> None:
    """
    Generate a win rate heatmap matrix where cell (A, B) shows
    the win rate of bot A against bot B. Save to output_path.
    """
    pass


def plot_win_rate_barchart(df: pd.DataFrame, output_path: str = "barchart.png") -> None:
    """
    Generate a bar chart showing the overall win rate of each variant
    across all matchups combined. Save to output_path.
    """
    pass


def generate_all(results_path: str = "experiments_results.csv") -> None:
    """Load results and generate all plots."""
    pass


if __name__ == "__main__":
    generate_all()
