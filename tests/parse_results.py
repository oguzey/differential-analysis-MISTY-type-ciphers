from conditions import Condition
from side import Side
from conditions import StateConditions
from variable import Variable
from variable import TypeVariable
from conditions import CustomConditions
from conditions import CompareCondition

a = Variable(TypeVariable.INPUT)
a2 = Variable(TypeVariable.INPUT)
a3 = Variable(TypeVariable.INPUT)

g1 = Variable(TypeVariable.OUTPUT)
g2 = Variable(TypeVariable.OUTPUT)
g3 = Variable(TypeVariable.OUTPUT)

# """ test of contradictions """
# test = Condition(Side(a), Side(), StateConditions.IS_ZERO)
# test2 = Condition(Side(a), Side(), StateConditions.IS_NOT_ZERO)
# assert test.is_contradiction(test2)

# test = Condition(Side(a, a2, g3), Side(), StateConditions.IS_ZERO)
# test2 = Condition(Side(a, a2, g3), Side(), StateConditions.IS_NOT_ZERO)
# assert test.is_contradiction(test2)

""" test of useless """
test = Condition(Side(), Side(), StateConditions.IS_ZERO)
assert test.is_useless()

test = Condition(Side(a, g3), Side(g3, a), StateConditions.IS_EQUAL)
assert test.is_useless()

test = Condition(Side(a, g3), Side(a, g3), StateConditions.IS_EQUAL)
assert test.is_useless()

test = Condition(Side(a, g3), Side(), StateConditions.IS_ZERO)
assert test.is_useless() == False

""" test of normalise """
test = Condition(Side(a, g3), Side(), StateConditions.IS_EQUAL)
test2 = Condition(Side(g3), Side(a), StateConditions.IS_EQUAL)
test.normalise()
assert test == test2

test = Condition(Side(), Side(a, g3), StateConditions.IS_EQUAL)
test2 = Condition(Side(g3), Side(a), StateConditions.IS_EQUAL)
test.normalise()
assert test == test2

""" test of swap """
test = Side(a, a3)
test2 = Side(g1, g2)
cond = Condition(test, test2, StateConditions.IS_EQUAL)
cond.swap_sides()
assert cond.get_left_side() == test2 and cond.get_right_side() == test

""" test of update"""
c = Condition(Side(a, a2, a3), Side(g1, a3), StateConditions.IS_EQUAL)
c1 = Condition(Side(a), Side(g3), StateConditions.IS_EQUAL)

c.update_with(c1)
c2 = Condition(Side(g3), Side(g1, a2), StateConditions.IS_EQUAL)

assert c == c2

c = Condition(Side(a, a2, a3), Side(a, g3), StateConditions.IS_EQUAL)
c1 = Condition(Side(a), Side(a2, a3), StateConditions.IS_EQUAL)
c2 = Condition(Side(g3), Side(a2, a3), StateConditions.IS_EQUAL)
c.update_with(c1)
assert c == c2

c = Condition(Side(a, a2, a3, g3), Side(), StateConditions.IS_NOT_ZERO)
c1 = Condition(Side(a), Side(a2, a3), StateConditions.IS_EQUAL)

c2 = Condition(Side(g3), Side(), StateConditions.IS_NOT_ZERO)
c.update_with(c1)

assert c == c2

c = Condition(Side(a, a2, a3, g3), Side(g2), StateConditions.IS_EQUAL)
c1 = Condition(Side(a, a2), Side(), StateConditions.IS_NOT_ZERO)

c2 = Condition(Side(a, a2, a3, g3), Side(g2), StateConditions.IS_EQUAL)
c.update_with(c1)

assert c == c2

"""test of compare """
c = Condition(Side(a, a2, a3, g3), Side(g2), StateConditions.IS_EQUAL)
c_copy = Condition(Side(a, a2, a3, g3), Side(g2), StateConditions.IS_EQUAL)
c2 = Condition(Side(a, a2, a3, g3, g2), Side(), StateConditions.IS_NOT_ZERO)
c2_copy = Condition(Side(a, a2, a3, g3, g2), Side(), StateConditions.IS_NOT_ZERO)
assert c.compare_conditions(c2) == CompareCondition.CONTRADICTION
assert c == c_copy and c2 == c2_copy


c = Condition(Side(a, g3), Side(), StateConditions.IS_ZERO)
c_copy = Condition(Side(a, g3), Side(), StateConditions.IS_ZERO)
c2 = Condition(Side(a, g3), Side(a2, a3, g2), StateConditions.IS_EQUAL)
c2_copy = Condition(Side(a, g3), Side(a2, a3, g2), StateConditions.IS_EQUAL)
assert c.compare_conditions(c2) == CompareCondition.NOT_EQUAL
assert c == c_copy and c2 == c2_copy

c = Condition(Side(a), Side(g3, g2), StateConditions.IS_EQUAL)
c_copy = Condition(Side(a), Side(g3, g2), StateConditions.IS_EQUAL)
c2 = Condition(Side(g3), Side(a, g2), StateConditions.IS_EQUAL)
c2_copy = Condition(Side(g3), Side(a, g2), StateConditions.IS_EQUAL)
assert c.compare_conditions(c2) == CompareCondition.EQUAL
assert c == c_copy and c2 == c2_copy

c = Condition(Side(a), Side(), StateConditions.IS_NOT_ZERO)
c2 = Condition(Side(g3), Side(), StateConditions.IS_NOT_ZERO)
assert c.compare_conditions(c2) == CompareCondition.NOT_EQUAL
"""  """

c = Condition(Side(a, a2, a3), Side(g1, a3), StateConditions.IS_EQUAL)
c1 = Condition(Side(a), Side(g3), StateConditions.IS_EQUAL)
c2 = Condition(Side(a, a2), Side(g1), StateConditions.IS_EQUAL)
# c1 = Condition(Side(a, a2), Side(g1), StateConditions.IS_ZERO)
c3 = Condition(Side(g3), Side(), StateConditions.IS_ZERO)
c4 = Condition(Side(g2), Side(), StateConditions.IS_ZERO)


cc = CustomConditions()

cc.append_condition(c)
print "after append 0 \n" + str(cc)
cc.append_condition(c1)
print "after append 1 \n" + str(cc)
cc.append_condition(c2)
print "after append 2 \n" + str(cc)
cc.append_condition(c3)
print "after append 3 \n" + str(cc)
cc.append_condition(c4)
print "after append 4 \n" + str(cc)



