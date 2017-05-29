from counter import Counter
from enum import Enum
from typing import Optional


class NodeType(Enum):
    ROOT = 0,   # first system
    FORK = 1,   # add to marks
    BRANCH = 2, # choose maximum mark
    LEAF = 3    # estimated system
    FINAL = 4   # internal using

    def __str__(self) -> str:
        return self.name


class Node(object):
    def __init__(self, sid: int, psid: int, ntype: Optional[NodeType]):
        self._sid = sid             # type: int
        self._psid = psid           # type: int
        self._node_type = ntype     # type: NodeType
        self._mark = None

    def set_node_type(self, ntype: NodeType):
        self._node_type = ntype

    def get_sid(self) -> int:
        return self._sid


class Collector(object):
    def __init__(self):
        self._counter_sid = Counter()
        self._nodes = dict()

    def create_root_node(self):
        sid = self._counter_sid.increment()
        return Node(sid, 0, NodeType.ROOT)

    def create_children(self, parent_node: Node):
        psid = parent_node.get_sid()
        child1 = Node(self._counter_sid.increment(), psid, None)
        child2 = Node(self._counter_sid.increment(), psid, None)
        return child1, child2

    def set_parent_type(self, parent_node: Node, node_type: NodeType) -> None:
        assert node_type == NodeType.FORK or node_type == NodeType.BRANCH
        parent_node.set_node_type(node_type)




