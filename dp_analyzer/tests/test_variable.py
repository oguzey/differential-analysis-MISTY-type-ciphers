import pytest

from variable import *


def test_variable_hash():
    assert hash(Variable(VariableType.INPUT)) == 1
    assert hash(Variable(VariableType.INPUT)) == 2

    assert hash(Variable(VariableType.OUTPUT)) == 1000000001
    assert hash(Variable(VariableType.OUTPUT)) == 1000000002

    assert hash(Variable(VariableType.UNKNOWN)) == 2000000001
    assert hash(Variable(VariableType.UNKNOWN)) == 2000000002
