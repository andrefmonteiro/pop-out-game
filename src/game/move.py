from dataclasses import dataclass
from enum import Enum

MoveType = Enum('MoveType', [("DROP", "d"), ("POP", "p")])

@dataclass
class Move: # acting basically as a named tuple
	move_type: MoveType
	col: int