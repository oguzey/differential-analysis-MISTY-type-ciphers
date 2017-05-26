from condition import Condition
from side import Side
from condition import ConditionState
from variable import Variable
from variable import VariableType
from condition import CustomConditions
from condition import CompareCondition

a = Variable(VariableType.INPUT)
a2 = Variable(VariableType.INPUT)
a3 = Variable(VariableType.INPUT)

g1 = Variable(VariableType.OUTPUT)
g2 = Variable(VariableType.OUTPUT)
g3 = Variable(VariableType.OUTPUT)

# """ test of contradictions """
# test = Condition(Side(a), Side(), StateConditions.IS_ZERO)
# test2 = Condition(Side(a), Side(), StateConditions.IS_NOT_ZERO)
# assert test.is_contradiction(test2)

# test = Condition(Side(a, a2, g3), Side(), StateConditions.IS_ZERO)
# test2 = Condition(Side(a, a2, g3), Side(), StateConditions.IS_NOT_ZERO)
# assert test.is_contradiction(test2)

""" test of useless """
test = Condition(Side(), Side(), ConditionState.IS_ZERO)
assert test.is_useless()

test = Condition(Side(a, g3), Side(g3, a), ConditionState.IS_EQUAL)
assert test.is_useless()

test = Condition(Side(a, g3), Side(a, g3), ConditionState.IS_EQUAL)
assert test.is_useless()

test = Condition(Side(a, g3), Side(), ConditionState.IS_ZERO)
assert test.is_useless() == False

""" test of normalise """
test = Condition(Side(a, g3), Side(), ConditionState.IS_EQUAL)
test2 = Condition(Side(g3), Side(a), ConditionState.IS_EQUAL)
test.normalise()
assert test == test2

test = Condition(Side(), Side(a, g3), ConditionState.IS_EQUAL)
test2 = Condition(Side(g3), Side(a), ConditionState.IS_EQUAL)
test.normalise()
assert test == test2

""" test of swap """
test = Side(a, a3)
test2 = Side(g1, g2)
cond = Condition(test, test2, ConditionState.IS_EQUAL)
cond.swap_sides()
assert cond.get_left_side() == test2 and cond.get_right_side() == test

""" test of update"""
c = Condition(Side(a, a2, a3), Side(g1, a3), ConditionState.IS_EQUAL)
c1 = Condition(Side(a), Side(g3), ConditionState.IS_EQUAL)

c.update_with(c1)
c2 = Condition(Side(g3), Side(g1, a2), ConditionState.IS_EQUAL)

assert c == c2

c = Condition(Side(a, a2, a3), Side(a, g3), ConditionState.IS_EQUAL)
c1 = Condition(Side(a), Side(a2, a3), ConditionState.IS_EQUAL)
c2 = Condition(Side(g3), Side(a2, a3), ConditionState.IS_EQUAL)
c.update_with(c1)
assert c == c2

c = Condition(Side(a, a2, a3, g3), Side(), ConditionState.IS_NOT_ZERO)
c1 = Condition(Side(a), Side(a2, a3), ConditionState.IS_EQUAL)

c2 = Condition(Side(g3), Side(), ConditionState.IS_NOT_ZERO)
c.update_with(c1)

assert c == c2

c = Condition(Side(a, a2, a3, g3), Side(g2), ConditionState.IS_EQUAL)
c1 = Condition(Side(a, a2), Side(), ConditionState.IS_NOT_ZERO)

c2 = Condition(Side(a, a2, a3, g3), Side(g2), ConditionState.IS_EQUAL)
c.update_with(c1)

assert c == c2

"""test of compare """
c = Condition(Side(a, a2, a3, g3), Side(g2), ConditionState.IS_EQUAL)
c_copy = Condition(Side(a, a2, a3, g3), Side(g2), ConditionState.IS_EQUAL)
c2 = Condition(Side(a, a2, a3, g3, g2), Side(), ConditionState.IS_NOT_ZERO)
c2_copy = Condition(Side(a, a2, a3, g3, g2), Side(), ConditionState.IS_NOT_ZERO)
assert c.compare_conditions(c2) == CompareCondition.CONTRADICTION
assert c == c_copy and c2 == c2_copy


c = Condition(Side(a, g3), Side(), ConditionState.IS_ZERO)
c_copy = Condition(Side(a, g3), Side(), ConditionState.IS_ZERO)
c2 = Condition(Side(a, g3), Side(a2, a3, g2), ConditionState.IS_EQUAL)
c2_copy = Condition(Side(a, g3), Side(a2, a3, g2), ConditionState.IS_EQUAL)
assert c.compare_conditions(c2) == CompareCondition.NOT_EQUAL
assert c == c_copy and c2 == c2_copy

c = Condition(Side(a), Side(g3, g2), ConditionState.IS_EQUAL)
c_copy = Condition(Side(a), Side(g3, g2), ConditionState.IS_EQUAL)
c2 = Condition(Side(g3), Side(a, g2), ConditionState.IS_EQUAL)
c2_copy = Condition(Side(g3), Side(a, g2), ConditionState.IS_EQUAL)
assert c.compare_conditions(c2) == CompareCondition.EQUAL
assert c == c_copy and c2 == c2_copy

c = Condition(Side(a), Side(), ConditionState.IS_NOT_ZERO)
c2 = Condition(Side(g3), Side(), ConditionState.IS_NOT_ZERO)
assert c.compare_conditions(c2) == CompareCondition.NOT_EQUAL
"""  """

c = Condition(Side(a, a2, a3), Side(g1, a3), ConditionState.IS_EQUAL)
c1 = Condition(Side(a), Side(g3), ConditionState.IS_EQUAL)
c2 = Condition(Side(a, a2), Side(g1), ConditionState.IS_EQUAL)
# c1 = Condition(Side(a, a2), Side(g1), StateConditions.IS_ZERO)
c3 = Condition(Side(g3), Side(), ConditionState.IS_ZERO)
c4 = Condition(Side(g2), Side(), ConditionState.IS_ZERO)


cc = CustomConditions()

cc.append_condition(c)
print("after append 0 \n" + str(cc))
cc.append_condition(c1)
print("after append 1 \n" + str(cc))
cc.append_condition(c2)
print("after append 2 \n" + str(cc))
cc.append_condition(c3)
print("after append 3 \n" + str(cc))
cc.append_condition(c4)
print("after append 4 \n" + str(cc))



