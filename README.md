# pop-out-game

Implementation of a PopOut playing bot, using MCTS and a decision tree (ID3).

## Setup

One-time, from the repo root:

```bash
python3 -m venv venv
source venv/bin/activate
pip install numpy pandas matplotlib seaborn
```

## Activate venv (each new terminal)

```bash
source venv/bin/activate
```

## Play the game

```bash
venv/bin/python main.py
```

## Key files

| File | Purpose |
|---|---|
| `todo.md` | Task checklist — start here |
| `notebook_notes.md` | Discussion points, metrics and talking points for the notebook |
| `src/mcts/mcts.py` | MCTS algorithm with UCT |
| `src/decision_tree/decision_tree_id3.py` | ID3 algorithm — fully implemented, runnable |
| `src/mcts_tournament/tournament.py` | Tournament runner (already done, results in CSV) |
| `src/mcts_tournament/visualize.py` | Tournament result plots |
| `src/decision_tree/visualize_id3.py` | ID3 result plot |
| `datasets/iris-dataset.csv` | Iris warm-up dataset |
| `popout_dataset.csv` | Generated PopOut dataset (15k+ rows, DT-Wide self-play) |
| `first_tournament_results.csv` | T1 results |
| `second_tournament_results.csv` | T2 results |

## Run ID3 on iris (smoke test)

```bash
venv/bin/python src/decision_tree/decision_tree_id3.py
```

Prints the iris decision tree and accuracy. Should finish in under 1 second.

## Run ID3 depth sweep on PopOut

See the `# TODO for notebook / coworkers` block at the bottom of
`src/decision_tree/decision_tree_id3.py` for the exact code to paste into a notebook cell.

This saves `id3_popout_results.csv` at the repo root — the results are persisted so you
never need to re-run the model just to regenerate a chart.

To regenerate the accuracy-vs-depth bar chart at any time (reads from the saved CSV):

```bash
venv/bin/python src/decision_tree/visualize_id3.py
```

Output: `src/decision_tree/graphs/popout_accuracy_vs_depth.png`

## Generate more MCTS dataset (optional — already at 15k rows)

```bash
venv/bin/python main_datasets.py
```

Appends DT-Wide vs DT-Wide game rows to `popout_dataset.csv`. Game IDs continue automatically.