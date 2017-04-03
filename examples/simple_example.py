import sys, os
sys.path.append("dp_analyzer")

from variable import Variable, TypeVariable
from side import Side
from transition import Transition, BlockFunction
from logger import logger

a = Variable(TypeVariable.INPUT)
b = Variable(TypeVariable.OUTPUT)
c = Variable(TypeVariable.UNKNOWN)

x = Side(a, b)
y = Side(a, c)

z = Transition(x, y, BlockFunction('F', 'p'))

logger.info("transition: {}".format(z))
