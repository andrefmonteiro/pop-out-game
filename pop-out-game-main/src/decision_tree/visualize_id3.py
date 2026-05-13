"""Visualisation for ID3 results on the PopOut dataset.
(Versão corrigida para nomes curtos)
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import matplotlib.pyplot as plt

GRAPHS_DIR = os.path.join(os.path.dirname(__file__), 'graphs')

def load_results(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)

def plot_accuracy_vs_depth(df: pd.DataFrame, output_path: str = None) -> None:
    """Bar chart of test accuracy per max_depth value."""
    if output_path is None:
        os.makedirs(GRAPHS_DIR, exist_ok=True)
        output_path = os.path.join(GRAPHS_DIR, 'popout_accuracy_vs_depth.png')

    df = df.copy()
    df['max_depth'] = df['max_depth'].fillna('unlimited').astype(str)

    _, ax = plt.subplots(figsize=(8, 5))
    
    # MUDANÇA AQUI: de 'test_accuracy' para 'test_acc'
    bars = ax.bar(df['max_depth'], df['test_acc'], color='steelblue', edgecolor='white')

    # MUDANÇA AQUI: de 'test_accuracy' para 'test_acc'
    for bar, acc in zip(bars, df['test_acc']):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            f'{acc:.2f}',
            ha='center', va='bottom', fontsize=10,
        )

    ax.set_ylim(0, 0.5) # Ajustei o limite para os teus 27% ficarem bem visíveis
    ax.set_xlabel('max_depth')
    ax.set_ylabel('Test accuracy')
    ax.set_title('ID3 on PopOut — test accuracy vs tree depth')
    
    # Linha de base (chance aleatória)
    ax.axhline(1 / 7, color='red', linestyle='--', linewidth=1, label='random baseline (~14%)')
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f'Plot saved to {output_path}')

def generate_all(results_path: str = 'id3_popout_results.csv') -> None:
    df = load_results(results_path)
    plot_accuracy_vs_depth(df)

if __name__ == "__main__":
    generate_all()