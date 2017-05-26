import pytest
from variable import Variable, VariableType
import side


def setup_module(module):
    global a_in
    global b_out
    global n_unk
    a_in = Variable(VariableType.INPUT)
    b_out = Variable(VariableType.OUTPUT)
    n_unk = Variable(VariableType.UNKNOWN)


def test_side_equal():
    a = Variable(VariableType.INPUT)
    b = Variable(VariableType.INPUT)
    c = Variable(VariableType.OUTPUT)
    d = Variable(VariableType.UNKNOWN)

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


def test_side_str():
    global a_in
    global b_out
    global n_unk
    x = side.Side(a_in, b_out, n_unk)
    assert str(x) == "[Input : 1] ⊕ [Output : 1] ⊕ [Unknown : 1]"


def test_side_contains_side():
    x = side.Side(a_in, b_out, n_unk)
    y = side.Side(a_in, a_in, b_out, n_unk)
