# pop-out-game

Implementation of a PopOut playing bot, using MCTS and a decision tree.

## Setup

One-time, from the repo root:

```bash
python3 -m venv venv
source venv/bin/activate
pip install numpy
```

## Run

Activate the venv first (each new terminal):

```bash
source venv/bin/activate
```

Play the game:

```bash
python main.py
```

## Generate MCTS dataset

```bash
python main_datasets.py
```

Runs 50 Bot-vs-Bot games and appends `(state, move)` rows to `popout_dataset.csv` for the decision-tree (ID3) part of the assignment.