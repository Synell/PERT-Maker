#----------------------------------------------------------------------

    # Libraries
from .path import Path
from .__debug__ import Debug
from .__error__ import Error

from data.lib.dimensionalEnv.vectors.vector2 import Vector2
#----------------------------------------------------------------------

    # Class
class Node: pass

class Node:
    def __init__(self, name: str = None, next: dict[str: Path] = {}, previous: dict[str: Node] = {}, minTime: float = 0, maxTime: float = 0, pos: Vector2 = Vector2()) -> None:
        if not name: raise Error('A node name cannot be empty!')
        self.name = name
        self.next = next
        self.previous = previous
        self.pos = pos
        self.minTime = minTime
        self.maxTime = maxTime
#----------------------------------------------------------------------
