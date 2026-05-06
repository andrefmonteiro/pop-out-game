import math
import random
import csv
import copy
from dataclasses import dataclass
from game.board import Board


@dataclass
class MCTSConfig:
    # Bundle of knobs that defines an MCTS "variant" so the tournament
    # can spawn several bots that differ only by their config values.
    name: str = "Default"          # human-readable label e.g. "Baseline"
    iterations: int = 1000         # how many MCTS iterations per move
    c: float = 1.414               # UCT exploration constant
    expansion_count: int = 1       # how many children to expand per iteration


class MCTSNode:
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        # Legal moves provided by Board
        self.untried_moves = board.get_legal_moves()

    def uct_value(self, c=1.414):
        if self.visits == 0:
            return float('inf')
        # UCT: exploitation + exploration
        return (self.wins / self.visits) + c * math.sqrt(math.log(self.parent.visits) / self.visits)


def _simulate_and_backprop(start_node, root_player):
    # Random playout from start_node.board, then walk back to the root
    # crediting wins/visits. Factored out so the iteration loop can call
    # it once per expanded child when expansion_count > 1.
    sim_board = copy.deepcopy(start_node.board)
    while sim_board.get_winner() is None:
        possible_moves = sim_board.get_legal_moves()
        if not possible_moves:
            break
        sim_board = sim_board.apply_move(random.choice(possible_moves))

    result = sim_board.get_winner()
    node = start_node
    while node:
        node.visits += 1
        # Win for the player who started the MCTS search
        if result == root_player:
            node.wins += 1
        elif result == 0:  # Draw
            node.wins += 0.5
        node = node.parent


def mcts_search(root_board, config: MCTSConfig):
    root_node = MCTSNode(root_board)

    for _ in range(config.iterations):
        node = root_node

        # 1. SELECTION
        while not node.untried_moves and node.children:
            node = max(node.children, key=lambda n: n.uct_value(config.c))

        # 2. EXPANSION (+ 3. SIMULATION + 4. BACKPROPAGATION per expanded child)
        if node.untried_moves:
            # Expand up to expansion_count children, or however many untried
            # moves remain. Each expanded child gets its own playout, so a
            # "wide" config (expansion_count > 1) does multiple rollouts per
            # iteration -- that means more total compute, not just a wider tree.
            n_expand = min(config.expansion_count, len(node.untried_moves))
            for _ in range(n_expand):
                move = node.untried_moves.pop()
                new_state = node.board.apply_move(move)
                child_node = MCTSNode(new_state, parent=node, move=move)
                node.children.append(child_node)
                _simulate_and_backprop(child_node, root_board.current_player)
        else:
            # Terminal selected node (no untried moves and no children either):
            # nothing to expand, so simulate from the node itself. Matches the
            # behaviour of the original single-expansion code.
            _simulate_and_backprop(node, root_board.current_player)

    # Pick the move with the most visits
    best_child = max(root_node.children, key=lambda n: n.visits)

    # Disabled while running tournaments so we don't bloat popout_dataset.csv
    # with thousands of bot-vs-bot decisions. Re-enable when generating
    # training data for the ID3 decision tree.
    # save_to_dataset(root_board, best_child.move)

    return best_child.move


def save_to_dataset(board, move):
    # Flatten the board (42 cells) and append the chosen move
    data = board.grid.flatten().tolist()
    move_str = f"{move.move_type.name}_{move.col}"
    with open('popout_dataset.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data + [move_str])
