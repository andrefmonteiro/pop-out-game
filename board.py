import numpy as np
from game.move import Move, MoveType

class Board:
    def __init__(self):
        # 6x7 board backed by NumPy
        self.current_player = 1
        self.grid = np.zeros((6, 7), dtype=np.uint8)
        
        # NOVO: Caderno de notas para a regra das 3 repetições (Empate).
        estado_inicial = (self.grid.tobytes(), self.current_player)
        self.state_history = {estado_inicial: 1}

    def get_legal_moves(self) -> list[Move]:
        moves = []
        # 1. DROP: columns whose top row (0) is empty
        for c in range(7):
            if self.grid[0, c] == 0:
                moves.append(Move(move_type=MoveType.DROP, col=c))

        # 2. POP: columns where the bottom piece (row 5) belongs to the current player
        for c in range(7):
            if self.grid[5, c] == self.current_player:
                moves.append(Move(move_type=MoveType.POP, col=c))
        return moves

    def apply_move(self, move: Move) -> 'Board':
        new_board = Board.__new__(Board)
        new_board.grid = self.grid.copy()
        new_board.current_player = self.current_player
        
        # NOVO: Passar o histórico para as cópias do MCTS não perderem a memória
        new_board.state_history = self.state_history.copy()

        if move.move_type == MoveType.DROP:
            for r in reversed(range(6)):
                if new_board.grid[r, move.col] == 0:
                    new_board.grid[r, move.col] = self.current_player
                    break

        elif move.move_type == MoveType.POP:
            # PopOut rule: remove the bottom piece and shift the column down
            new_board.grid[1:6, move.col] = new_board.grid[0:5, move.col]
            new_board.grid[0, move.col] = 0

        new_board.current_player = 3 - self.current_player
        
        # NOVO: Registar a nova fotografia no caderno de notas
        state_key = (new_board.grid.tobytes(), new_board.current_player)
        new_board.state_history[state_key] = new_board.state_history.get(state_key, 0) + 1
        
        return new_board

    def get_winner(self) -> int | None:
        # Player who just moved
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
            # Diagonals
            for r in range(3):
                for c in range(4):
                    if all(self.grid[r+i, c+i] == p for i in range(4)): return True
                    if all(self.grid[r+3-i, c+i] == p for i in range(4)): return True
            return False

        # Rule 1: if a pop creates a four-in-a-row for both players, the mover wins
        if check(last_player): return last_player
        if check(self.current_player): return self.current_player

        # Rule 2: draw if the board has no legal moves left
        if not self.get_legal_moves(): return 0
        
        # NOVO - Regra 3: Empate por tripla repetição (loops infinitos)
        estado_atual = (self.grid.tobytes(), self.current_player)
        if self.state_history.get(estado_atual, 0) >= 3:
            return 0  # 0 declara empate perante o vosso código do jogo

        return None

    def __str__(self):
        symbols = {0: ".", 1: "X", 2: "0"}
        header = " ".join(str(c + 1) for c in range(7))
        rows = "\n".join(" ".join(symbols[cell] for cell in row) for row in self.grid)
        return f"{header}\n{rows}"