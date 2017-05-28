from linear_operator import LOMu, LOLambda
from variable import Variable, VariableType
from transition import BlockFunction
from collections import namedtuple
from typing import Union

System = namedtuple('System', ['transitions', 'inputs', 'outputs'])


def cp_and_use_lo(var: Variable, op: Union[LOLambda, LOMu], op2: Union[LOLambda, LOMu]=None):
    tmp = var.clone()
    tmp.apply_lin_oper(op.clone())
    if op2 is not None:
        tmp.apply_lin_oper(op2.clone())
    return tmp


a1 = Variable(VariableType.INPUT)
a2 = Variable(VariableType.INPUT)
a3 = Variable(VariableType.INPUT)
a4 = Variable(VariableType.INPUT)
a5 = Variable(VariableType.INPUT)
a6 = Variable(VariableType.INPUT)
a7 = Variable(VariableType.INPUT)
a8 = Variable(VariableType.INPUT)


b1 = Variable(VariableType.UNKNOWN)
b2 = Variable(VariableType.UNKNOWN)
b3 = Variable(VariableType.UNKNOWN)
b4 = Variable(VariableType.UNKNOWN)
b5 = Variable(VariableType.UNKNOWN)

c1 = Variable(VariableType.OUTPUT)
c2 = Variable(VariableType.OUTPUT)
c3 = Variable(VariableType.OUTPUT)
c4 = Variable(VariableType.OUTPUT)
c5 = Variable(VariableType.OUTPUT)
c6 = Variable(VariableType.OUTPUT)
c7 = Variable(VariableType.OUTPUT)
c8 = Variable(VariableType.OUTPUT)

mu = LOMu()
lmbda = LOLambda()
F = BlockFunction('F', 'p')
G = BlockFunction('G', 'q')