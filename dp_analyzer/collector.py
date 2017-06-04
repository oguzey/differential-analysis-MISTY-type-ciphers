from counter import Counter
from enum import Enum
from typing import Optional, Dict, List
from sympy import Symbol
from logger import logger


class NodeType(Enum):
    ROOT = 0,   # first system
    FORK = 1,   # add to marks
    BRANCH = 2, # choose maximum mark
    LEAF = 3    # estimated system
    FINAL = 4   # internal using

    def __str__(self) -> str:
        return self.name


class Node(object):
    def __init__(self, sid: int, psid: int, ntype: Optional[NodeType], tree_depth: int):
        self._sid = sid                 # type: int
        self._psid = psid               # type: int
        self._node_type = ntype         # type: NodeType
        self._mark = None               # type: List[Symbol]
        self._tree_depth = tree_depth   # type: int

    def set_node_type(self, ntype: NodeType):
        self._node_type = ntype

    def set_mark(self, mark: List[Symbol]):
        assert mark is not None and isinstance(mark, List)
        self._mark = mark

    def get_mark(self) -> Optional[List[Symbol]]:
        return self._mark

    def get_sid(self) -> int:
        return self._sid

    def get_psid(self) -> int:
        return self._psid

    def get_tree_depth(self) -> int:
        return self._tree_depth

    def get_node_type(self) -> NodeType:
        return self._node_type


class Collector(object):
    def __init__(self):
        self._counter_sid = Counter()   # type: Counter
        self._nodes_by_sid = dict()     # type: Dict[int, Node]
        self._nodes_by_depth = dict()   # type: Dict[int, List[Node]]
        self._max_tree_depth = 0        # type: int

    def append_to_nodes(self, node: Node):
        sid = node.get_sid()
        tree_depth = node.get_tree_depth()

        assert self._nodes_by_sid.get(sid, None) is None

        self._nodes_by_sid[sid] = node
        if self._nodes_by_depth.get(tree_depth, None) is None:
            self._nodes_by_depth[tree_depth] = []
        self._nodes_by_depth[tree_depth].append(node)

        if tree_depth > self._max_tree_depth:
            self._max_tree_depth = tree_depth

    def create_root_node(self):
        sid = self._counter_sid.increment()
        root = Node(sid, 0, NodeType.ROOT, 1)
        logger.info("collector: root node with sid '{}' created".format(sid))
        return root

    def create_children(self, parent_node: Node):
        psid = parent_node.get_sid()
        tree_depth = parent_node.get_tree_depth() + 1
        child1 = Node(self._counter_sid.increment(), psid, None, tree_depth)
        child2 = Node(self._counter_sid.increment(), psid, None, tree_depth)
        logger.info("collector: children sid = [{}, {}], tree_depth = {} created".format(child1.get_sid(), child2.get_sid(), tree_depth))
        return child1, child2

    def make_parent_node(self, parent_node: Node, node_type: NodeType) -> None:
        assert node_type == NodeType.FORK or node_type == NodeType.BRANCH
        parent_node.set_node_type(node_type)
        logger.info("collector: parent node 'sid = {}' added as {}".format(parent_node.get_sid(), node_type))

    def make_node_leaf(self, leaf_node: Node, mark: Symbol):
        assert mark is not None

        if leaf_node.get_node_type() == NodeType.ROOT:
            logger.info("collector: root node '{}' add as leaf with mark '{}'".format(leaf_node.get_sid(), mark))
        else:
            assert leaf_node.get_node_type() is None
            leaf_node.set_node_type(NodeType.LEAF)
        leaf_node.set_mark([mark])
        logger.info("collector: leaf node '{}' added with mark '{}'".format(leaf_node.get_sid(), mark))

    def _reset(self) -> None:
        assert len(self._nodes_by_sid) == 0
        assert len(self._nodes_by_depth) == 0
        assert self._max_tree_depth == 0
        self._counter_sid.reset()

    def collect(self):
        assert self._max_tree_depth > 0

        while self._max_tree_depth > 1:
            self._remove_bottom_layer_tree()

        marks = []
        assert self._max_tree_depth == 1
        # no children
        nodes = self._nodes_by_depth[1]
        for node in nodes:
            assert node.get_node_type() in [NodeType.LEAF, NodeType.ROOT]
            node_mark = node.get_mark()
            assert node_mark is not None and len(node_mark) > 0
            marks.extend(node_mark)
            del self._nodes_by_sid[node.get_sid()]
        del self._nodes_by_depth[1]
        self._max_tree_depth -= 1
        self._reset()
        return marks

    def _remove_bottom_layer_tree(self):
        assert self._max_tree_depth > 1
        # have depth more than one
        nodes = self._nodes_by_depth[self._max_tree_depth]
        # parent => children
        parents = dict()    # type: Dict[int, List[Node]]

        for node in nodes:
            # should have only leafs
            # but probably some systems cannot be estimated, so we will get parent without children
            # just skip it
            psid = node.get_psid()
            if parents.get(psid, None) is None:
                parents[psid] = []
            parents[psid].append(node)
        logger.info("collector: found {} parents of {} childrens".format(len(parents), len(nodes)))
        for psid in parents.keys():
            children = parents[psid]
            assert 1 <= len(children) <= 2
            # get origin parent
            orig_parent = self._nodes_by_sid[psid]
            pmark = []
            if orig_parent.get_node_type() == NodeType.BRANCH:
                assert orig_parent.get_mark() is None
                for child in children:
                    cmark = child.get_mark()
                    if cmark is not None:
                        pmark.extend(cmark)
            else:
                assert orig_parent.get_node_type() == NodeType.FORK
                if len(children) == 1:
                    cmark = children[0].get_mark()
                    if cmark is not None:
                        pmark.extend(cmark)
                else:
                    cmark1, cmark2 = children[0].get_mark(), children[1].get_mark()
                    if cmark1 is None:
                        if cmark2 is None:
                            pass
                        else:
                            pmark.extend(cmark2)
                    else:  # cmark1 is not None
                        if cmark2 is None:
                            pmark.extend(cmark1)
                        else:
                            # cmark1 and cmark2 is not None
                            logger.info("collector: len(ch_mark1)={}, len(ch_mark2)={}".format(len(cmark1), len(cmark2)))
                            for m1 in cmark1:
                                for m2 in cmark2:
                                    logger.info("collector: fork parent append '{}' mark".format(m1 + m2))
                                    pmark.append(m1 + m2)

            orig_parent.set_mark(pmark)
            orig_parent.set_node_type(NodeType.LEAF)

        # remove nodes
        for node in nodes:
            del self._nodes_by_sid[node.get_sid()]
        # remove layer
        del self._nodes_by_depth[self._max_tree_depth]
        self._max_tree_depth -= 1
        logger.info("collector: max_tree_depth became {}".format(self._max_tree_depth))


collector = Collector()
