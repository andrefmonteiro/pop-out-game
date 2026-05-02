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
        # Pega os movimentos legais definidos no teu Board
        self.untried_moves = board.get_legal_moves()

    def uct_value(self, c=1.414):
        if self.visits == 0:
            return float('inf')
        # Fórmula UCT: Exploração vs Exploração
        return (self.wins / self.visits) + c * math.sqrt(math.log(self.parent.visits) / self.visits)

def mcts_search(root_board, iterations=1000):
    root_node = MCTSNode(root_board)

    for _ in range(iterations):
        node = root_node
        
        # 1. SELEÇÃO
        while not node.untried_moves and node.children:
            node = max(node.children, key=lambda n: n.uct_value())
        
        # 2. EXPANSÃO
        if node.untried_moves:
            move = node.untried_moves.pop()
            new_state = node.board.apply_move(move)
            child_node = MCTSNode(new_state, parent=node, move=move)
            node.children.append(child_node)
            node = child_node

        # 3. SIMULAÇÃO (Playout)
        sim_board = copy.deepcopy(node.board)
        while sim_board.get_winner() is None:
            possible_moves = sim_board.get_legal_moves()
            if not possible_moves: break
            sim_board = sim_board.apply_move(random.choice(possible_moves))
        
        # 4. RETROPROPAGAÇÃO[cite: 1]
        result = sim_board.get_winner()
        while node:
            node.visits += 1
            # Se o resultado for vitória do jogador que iniciou o MCTS
            if result == root_board.current_player:
                node.wins += 1
            elif result == 0: # Empate[cite: 1]
                node.wins += 0.5
            node = node.parent

    # Escolhe a jogada com mais visitas[cite: 1]
    best_child = max(root_node.children, key=lambda n: n.visits)
    
    # GUARDA DADOS PARA A ÁRVORE DE DECISÃO (ID3)[cite: 1]
    save_to_dataset(root_board, best_child.move)
    
    return best_child.move

def save_to_dataset(board, move):
    # Flatten do board (42 posições) + a jogada[cite: 1]
    data = board.grid.flatten().tolist()
    move_str = f"{move.move_type.name}_{move.col}"
    with open('popout_dataset.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data + [move_str])