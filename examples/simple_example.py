import sys
sys.path.append("dp_analyzer")

from variable import Variable, VariableType
from side import Side
from transition import Transition, BlockFunction
from logger import logger

a = Variable(VariableType.INPUT)
b = Variable(VariableType.OUTPUT)
c = Variable(VariableType.UNKNOWN)

x = Side(a, b)
y = Side(a, c)

z = Transition(x, y, BlockFunction('F', 'p'))

logger.info("transition: {}".format(z))
