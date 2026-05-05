from dataclasses import dataclass
from enum import Enum

# The two move types allowed in PopOut
MoveType = Enum('MoveType', [("DROP", "d"), ("POP", "p")])

@dataclass
class Move:
    # Lightweight container that carries a single move's information
    move_type: MoveType
    col: int
