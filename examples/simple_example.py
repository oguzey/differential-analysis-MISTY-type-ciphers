from variable import Variable, TypeVariable
from side import Side
from transition import Transition
from logger import logger

a = variable.Variable(TypeVariable.INPUT)
b = variable.Variable(TypeVariable.OUTPUT)
c = variable.Variable(TypeVariable.UNKNOWN)

x = Side(a, b)
y = Side(a, c)

z = Transition(x, y)

logger.info("transition: {}".format(z))
