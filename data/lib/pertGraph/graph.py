#----------------------------------------------------------------------

    # Libraries
from .path import Path
from .node import Node
from .__debug__ import Debug
from .__error__ import Error

from data.lib.dimensionalEnv.vectors.vector2 import Vector2
#----------------------------------------------------------------------

    # Class
class Graph:
    __TEMP_PATH_NAME__ = '&~#[|`\^@]TEMP_'
    def __init__(self) -> None:
        self.__nodes__ = {}

    def addNode(self, name: str = None, next: dict[str: float] = {}, previous: dict[str: float] = {}, minTime: float = 0, maxTime: float = 0, pos: Vector2 = Vector2()) -> None:
        for n in list(next.keys()):
            if not n in list(self.__nodes__.keys()): raise Error(f'This node doesn\'t exist! \'{n}\' in \'next\' is undefined.')
        for n in list(previous.keys()):
            if not n in list(self.__nodes__.keys()): raise Error(f'This node doesn\'t exist! \'{n}\' in \'previous\' is undefined.')

        if name in list(self.__nodes__.keys()): raise Error('A node with this name already exists!')

        self.__nodes__[name] = Node(name = name, next = {}, previous = {}, minTime = minTime, maxTime = maxTime, pos = pos)
        for n in list(next.keys()):
            self.__nodes__[name].next[n] = Path(node = self.__nodes__[n], value = next[n])
            self.__nodes__[n].previous[name] = self.__nodes__[name]

        for n in list(previous.keys()):
            self.__nodes__[n].next[name] = Path(node = self.__nodes__[name], value = previous[n])
            self.__nodes__[name].previous[n] = self.__nodes__[n]

    def removeNode(self, name: str = ''):
        if not (name in list(self.__nodes__.keys())): raise Error(f'This node doesn\'t exist! \'{name}\' is undefined.')
        for k in list(self.__nodes__.keys()):
            if name in list(self.__nodes__[k].next.keys()): del self.__nodes__[k].next[name]
            if name in list(self.__nodes__[k].previous.keys()): del self.__nodes__[k].previous[name]
        del self.__nodes__[name]

    def addConnection(self, from_: str = None, to_: str = None, name: str = '', value: float = 0) -> None:
        if not (from_ in list(self.__nodes__.keys())): raise Error(f'This node doesn\'t exist! \'{from_}\' is undefined.')
        if not (to_ in list(self.__nodes__.keys())): raise Error(f'This node doesn\'t exist! \'{to_}\' is undefined.')

        if to_ in list(self.__nodes__[from_].next.keys()): return Debug.warning(f'\'{from_}\' is already connected to \'{to_}\'!')

        self.__nodes__[from_].next[to_] = Path(node = self.__nodes__[to_], name = name, value = value)
        self.__nodes__[to_].previous[from_] = self.__nodes__[from_]

    def removeConnection(self, from_: str = None, to_: str = None) -> None:
        if not (from_ in list(self.__nodes__.keys())): raise Error(f'This node doesn\'t exist! \'{from_}\' is undefined.')
        if not (to_ in list(self.__nodes__.keys())): raise Error(f'This node doesn\'t exist! \'{to_}\' is undefined.')

        del self.__nodes__[from_].next[to_]
        del self.__nodes__[to_].previous[from_]


    def rename(self, oldNode: str = None, newNode: str = None):
        if type(oldNode) is not str or not (oldNode in list(self.__nodes__.keys())): raise Error(f'This node doesn\'t exist! \'{oldNode}\' is undefined.')
        if type(newNode) is not str: raise Error(f'This node cannot be created! \'{newNode}\' must be a str.')
        if newNode in list(self.__nodes__.keys()): raise Error(f'This node cannot be created! \'{newNode}\' already exists.')

        for node in list(self.__nodes__.keys()):
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

        path = self.__nodes__[oldNode]
        del self.__nodes__[oldNode]
        self.__nodes__[newNode] = path


    def findPath(self, from_: str = None, to_: str = None):
        if not (from_ in list(self.__nodes__.keys())): raise Error(f'This node doesn\'t exist! \'{from_}\' is undefined.')
        if not (to_ in list(self.__nodes__.keys())): raise Error(f'This node doesn\'t exist! \'{to_}\' is undefined.')

        from_, to_ = self.node(from_), self.node(to_)

        for next in list(from_.next.keys()):
            if from_.next[next].node.name == to_.name: return from_.next[next]


    def node(self, name: str = None) -> Node|None:
        if not name in list(self.__nodes__.keys()): return
        return self.__nodes__[name]

    @property
    def nodes(self) -> list[str]:
        return list(self.__nodes__.keys())


    def toDict(self) -> dict:
        def nodeToDict(node: Node):
            def pathToDict(path: Path):
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
                nodeResult['next'][p] = pathToDict(node.next[p])

            return nodeResult

        result = {}
        for n in list(self.__nodes__.keys()):
            result[n] = nodeToDict(self.__nodes__[n])

        return result


    def loadFromDict(self, dct: dict) -> None:
        self.__nodes__ = {}

        for n in list(dct.keys()):
            self.addNode(name = n, minTime = dct[n]['minTime'], maxTime = dct[n]['maxTime'], pos = Vector2(dct[n]['pos'][0], dct[n]['pos'][1]))

        for n in list(dct.keys()):
            for c in list(dct[n]['next'].keys()):
                self.addConnection(from_ = n, to_ = c, name = dct[n]['next'][c]['name'], value = dct[n]['next'][c]['value'])


    def setPathNamesAsNodeNames(self):
        for node in self.nodes:
            for path in list(self.__nodes__[node].next.keys()):
                if (not self.__nodes__[node].next[path].name) and (self.__nodes__[node].next[path].value):
                    self.__nodes__[node].next[path].name = self.__nodes__[node].name

    def resetPathNamesAsNodeNames(self):
        for node in self.nodes:
            for path in list(self.__nodes__[node].next.keys()):
                self.__nodes__[node].next[path].name = ''
#----------------------------------------------------------------------
