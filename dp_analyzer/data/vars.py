from linear_operator import LOMu, LOLambda
from variable import Variable, VariableType
from transition import BlockFunction, Transition
from collections import namedtuple
from typing import Union, List

System = namedtuple('System', ['transitions', 'inputs', 'outputs'])


def clone_with_use_oper(var: Variable, op: Union[LOLambda, LOMu]):
    tmp = var.clone()
    tmp.apply_lin_oper(op)
    return tmp


a1 = Variable(VariableType.INPUT)
a2 = Variable(VariableType.INPUT)

b1 = Variable(VariableType.UNKNOWN)

c1 = Variable(VariableType.OUTPUT)
c2 = Variable(VariableType.OUTPUT)

mu = LOMu()
lmbda = LOLambda()
F = BlockFunction('F', 'p')
G = BlockFunction('G', 'q')