import math
import random
import csv
import copy
from game.board import Board

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

def mcts_search(root_board, iterations=1000):
    root_node = MCTSNode(root_board)

    for _ in range(iterations):
        node = root_node

        # 1. SELECTION
        while not node.untried_moves and node.children:
            node = max(node.children, key=lambda n: n.uct_value())

        # 2. EXPANSION
        if node.untried_moves:
            move = node.untried_moves.pop()
            new_state = node.board.apply_move(move)
            child_node = MCTSNode(new_state, parent=node, move=move)
            node.children.append(child_node)
            node = child_node

        # 3. SIMULATION (playout)
        sim_board = copy.deepcopy(node.board)
        while sim_board.get_winner() is None:
            possible_moves = sim_board.get_legal_moves()
            if not possible_moves: break
            sim_board = sim_board.apply_move(random.choice(possible_moves))

        # 4. BACKPROPAGATION
        result = sim_board.get_winner()
        while node:
            node.visits += 1
            # Win for the player who started the MCTS search
            if result == root_board.current_player:
                node.wins += 1
            elif result == 0:  # Draw
                node.wins += 0.5
            node = node.parent

    # Pick the move with the most visits
    best_child = max(root_node.children, key=lambda n: n.visits)

    # Save the (state, move) pair for the decision-tree (ID3) dataset
    save_to_dataset(root_board, best_child.move)

    return best_child.move

def save_to_dataset(board, move):
    # Flatten the board (42 cells) and append the chosen move
    data = board.grid.flatten().tolist()
    move_str = f"{move.move_type.name}_{move.col}"
    with open('popout_dataset.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data + [move_str])
