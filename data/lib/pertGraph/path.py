#----------------------------------------------------------------------

    # Class
class Node: pass

class Path:
    def __init__(self, node: Node, name: str = '', value: float = 0) -> None:
        self.node = node
        self.name = name
        self.value = value
#----------------------------------------------------------------------
