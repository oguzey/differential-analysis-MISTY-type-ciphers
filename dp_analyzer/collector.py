from counter import Counter
from enum import Enum


class NodeType(Enum):
    ROOT = 0,   # first system
    FORK = 1,   # add to marks
    BRANCH = 2, # choose maximum mark
    LEAF = 3    # estimated system
    FINAL = 4   # internal using

    def __str__(self) -> str:
        return self.name


class Node(object):
    def __init__(self, sid: int, psid: int, ntype: NodeType):
        self._sid = sid             # type: int
        self._psid = psid           # type: int
        self._node_type = ntype     # type: NodeType
        self._mark = None

    def set_node_type(self, ntype: NodeType):
        self._node_type = ntype

    def create_child(self):
        child = Node()


class Collector(object):
    def __init__(self):
        self._counter_sid = Counter()

    def create_root_node(self):
        sid = self._counter_sid.increment()
        return Node(sid, 0, NodeType.ROOT)

    def create_сhildren(self, node: Node):
        pass


