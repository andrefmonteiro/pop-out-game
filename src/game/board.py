import numpy as np
import copy
from game.move import Move, MoveType

class Board:
    def __init__(self):
        # Inicialização com NumPy 6x7
        self.current_player = 1
        self.grid = np.zeros((6, 7), dtype=np.uint8)

    def get_legal_moves(self) -> list[Move]:
        moves = []
        # 1. DROP: Colunas onde a linha do topo (0) está vazia
        for c in range(7):
            if self.grid[0, c] == 0:
                moves.append(Move(move_type=MoveType.DROP, col=c))
        
        # 2. POP: Colunas onde a peça do fundo (linha 5) é do jogador atual
        for c in range(7):
            if self.grid[5, c] == self.current_player:
                moves.append(Move(move_type=MoveType.POP, col=c))
        return moves

    def apply_move(self, move: Move) -> 'Board':
        # Criar cópia para o MCTS simular sem alterar o jogo real
        new_board = copy.deepcopy(self)
        
        if move.move_type == MoveType.DROP:
            for r in reversed(range(6)):
                if new_board.grid[r, move.col] == 0:
                    new_board.grid[r, move.col] = self.current_player
                    break
        
        elif move.move_type == MoveType.POP:
            # Regra PopOut: remove o fundo e desce as peças acima
            new_board.grid[1:6, move.col] = new_board.grid[0:5, move.col]
            new_board.grid[0, move.col] = 0
            
        new_board.current_player = 3 - self.current_player
        return new_board

    def get_winner(self) -> int | None:
        # Jogador que acabou de jogar
        last_player = 3 - self.current_player
        
        def check(p):
            # Horizontal
            for r in range(6):
                for c in range(4):
                    if np.all(self.grid[r, c:c+4] == p): return True
            # Vertical
            for r in range(3):
                for c in range(7):
                    if np.all(self.grid[r:r+4, c] == p): return True
            # Diagonais
            for r in range(3):
                for c in range(4):
                    if all(self.grid[r+i, c+i] == p for i in range(4)): return True
                    if all(self.grid[r+3-i, c+i] == p for i in range(4)): return True
            return False

        # Regra 1: Se o pop criar 4-em-linha para ambos, quem moveu ganha
        if check(last_player): return last_player
        if check(self.current_player): return self.current_player
        
        # Regra 2: Empate se o board estiver cheio
        if not self.get_legal_moves(): return 0
        
        return None

    def __str__(self):
        symbols = {0: ".", 1: "X", 2: "0"}
        return "\n".join(" ".join(symbols[cell] for cell in row) for row in self.grid)