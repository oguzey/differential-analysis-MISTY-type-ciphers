import pytest
from variable import Variable, TypeVariable
import side


def test_side_equal():
    a = Variable(TypeVariable.INPUT)
    b = Variable(TypeVariable.INPUT)
    c = Variable(TypeVariable.OUTPUT)
    d = Variable(TypeVariable.UNKNOWN)

    x = side.Side(a, a, b, c)
    y = side.Side(a, b, b, c)
    assert (x == y) == False

    x = side.Side(a, d)
    y = side.Side(a, d)
    assert x == y

    x = side.Side(b)
    y = side.Side(d)
    assert (x == y) == False

    x = side.Side()
    y = side.Side()
    assert x == y
