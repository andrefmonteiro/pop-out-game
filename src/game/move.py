from dataclasses import dataclass
from enum import Enum

# Define os dois tipos de jogada permitidos no PopOut
MoveType = Enum('MoveType', [("DROP", "d"), ("POP", "p")])

@dataclass
class Move: 
    # Esta classe serve apenas para transportar a informação da jogada
    move_type: MoveType
    col: int