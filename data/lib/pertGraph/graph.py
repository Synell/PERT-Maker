#----------------------------------------------------------------------

    # Libraries
from .path import Path
from .node import Node
from .__debug__ import Debug
from .__error__ import Error

from data.lib.extendedmath import Vector2
#----------------------------------------------------------------------

    # Class
class Graph:
    _TEMP_PATH_NAME = '&~#[|`\^@]TEMP_'
    def __init__(self) -> None:
        self._nodes = {}

    def add_node(self, name: str = None, next: dict[str: float] = {}, previous: dict[str: float] = {}, minTime: float = 0, maxTime: float = 0, pos: Vector2 = Vector2()) -> None:
        for n in list(next.keys()):
            if not n in list(self._nodes.keys()): raise Error(f'This node doesn\'t exist! \'{n}\' in \'next\' is undefined.')
        for n in list(previous.keys()):
            if not n in list(self._nodes.keys()): raise Error(f'This node doesn\'t exist! \'{n}\' in \'previous\' is undefined.')

        if name in list(self._nodes.keys()): raise Error('A node with this name already exists!')

        self._nodes[name] = Node(name = name, next = {}, previous = {}, minTime = minTime, maxTime = maxTime, pos = pos)
        for n in list(next.keys()):
            self._nodes[name].next[n] = Path(node = self._nodes[n], value = next[n])
            self._nodes[n].previous[name] = self._nodes[name]

        for n in list(previous.keys()):
            self._nodes[n].next[name] = Path(node = self._nodes[name], value = previous[n])
            self._nodes[name].previous[n] = self._nodes[n]

    def remove_node(self, name: str = ''):
        if not (name in list(self._nodes.keys())): raise Error(f'This node doesn\'t exist! \'{name}\' is undefined.')
        for k in list(self._nodes.keys()):
            if name in list(self._nodes[k].next.keys()): del self._nodes[k].next[name]
            if name in list(self._nodes[k].previous.keys()): del self._nodes[k].previous[name]
        del self._nodes[name]

    def add_connection(self, from_: str = None, to_: str = None, name: str = '', value: float = 0) -> None:
        if not (from_ in list(self._nodes.keys())): raise Error(f'This node doesn\'t exist! \'{from_}\' is undefined.')
        if not (to_ in list(self._nodes.keys())): raise Error(f'This node doesn\'t exist! \'{to_}\' is undefined.')

        if to_ in list(self._nodes[from_].next.keys()): return Debug.warning(f'\'{from_}\' is already connected to \'{to_}\'!')

        self._nodes[from_].next[to_] = Path(node = self._nodes[to_], name = name, value = value)
        self._nodes[to_].previous[from_] = self._nodes[from_]

    def remove_connection(self, from_: str = None, to_: str = None) -> None:
        if not (from_ in list(self._nodes.keys())): raise Error(f'This node doesn\'t exist! \'{from_}\' is undefined.')
        if not (to_ in list(self._nodes.keys())): raise Error(f'This node doesn\'t exist! \'{to_}\' is undefined.')

        del self._nodes[from_].next[to_]
        del self._nodes[to_].previous[from_]


    def rename(self, oldNode: str = None, newNode: str = None):
        if type(oldNode) is not str or not (oldNode in list(self._nodes.keys())): raise Error(f'This node doesn\'t exist! \'{oldNode}\' is undefined.')
        if type(newNode) is not str: raise Error(f'This node cannot be created! \'{newNode}\' must be a str.')
        if newNode in list(self._nodes.keys()): raise Error(f'This node cannot be created! \'{newNode}\' already exists.')

        for node in list(self._nodes.keys()):
            if self.node(node).name == oldNode: self.node(node).name = newNode

            for next in list(self.node(node).next.keys()):
                if next == oldNode:
                    path = self.node(node).next[next]
                    del self.node(node).next[next]
                    self.node(node).next[newNode] = path

            for previous in list(self.node(node).previous.keys()):
                if previous == oldNode:
                    path = self.node(node).previous[previous]
                    del self.node(node).previous[previous]
                    self.node(node).previous[newNode] = path

        path = self._nodes[oldNode]
        del self._nodes[oldNode]
        self._nodes[newNode] = path


    def find_path(self, from_: str = None, to_: str = None):
        if not (from_ in list(self._nodes.keys())): raise Error(f'This node doesn\'t exist! \'{from_}\' is undefined.')
        if not (to_ in list(self._nodes.keys())): raise Error(f'This node doesn\'t exist! \'{to_}\' is undefined.')

        from_, to_ = self.node(from_), self.node(to_)

        for next in list(from_.next.keys()):
            if from_.next[next].node.name == to_.name: return from_.next[next]


    def node(self, name: str = None) -> Node|None:
        if not name in list(self._nodes.keys()): return
        return self._nodes[name]

    @property
    def nodes(self) -> list[str]:
        return list(self._nodes.keys())


    def to_dict(self) -> dict:
        def node_to_dict(node: Node):
            def path_to_dict(path: Path):
                return {
                    'name': path.name,
                    'value': path.value,
                    'node': path.node.name
                }

            nodeResult = {
                'name': node.name,
                'next': {},
                'minTime': node.minTime,
                'maxTime': node.maxTime,
                'pos': [node.pos.x, node.pos.y]
            }
            for p in list(node.next.keys()):
                nodeResult['next'][p] = path_to_dict(node.next[p])

            return nodeResult

        result = {}
        for n in list(self._nodes.keys()):
            result[n] = node_to_dict(self._nodes[n])

        return result


    def load_from_dict(self, dct: dict) -> None:
        self._nodes = {}

        for n in list(dct.keys()):
            self.add_node(name = n, minTime = dct[n]['minTime'], maxTime = dct[n]['maxTime'], pos = Vector2(dct[n]['pos'][0], dct[n]['pos'][1]))

        for n in list(dct.keys()):
            for c in list(dct[n]['next'].keys()):
                self.add_connection(from_ = n, to_ = c, name = dct[n]['next'][c]['name'], value = dct[n]['next'][c]['value'])


    def set_path_names_as_node_names(self):
        for node in self.nodes:
            for path in list(self._nodes[node].next.keys()):
                if (not self._nodes[node].next[path].name) and (self._nodes[node].next[path].value):
                    self._nodes[node].next[path].name = self._nodes[node].name

    def reset_path_names_as_node_names(self):
        for node in self.nodes:
            for path in list(self._nodes[node].next.keys()):
                self._nodes[node].next[path].name = ''
#----------------------------------------------------------------------
