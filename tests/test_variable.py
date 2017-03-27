import pytest

from variable import *


def test_variable_hash():
    assert hash(Variable(TypeVariable.INPUT)) == 1
    assert hash(Variable(TypeVariable.INPUT)) == 2

    assert hash(Variable(TypeVariable.OUTPUT)) == 1000001
    assert hash(Variable(TypeVariable.OUTPUT)) == 1000002

    assert hash(Variable(TypeVariable.UNKNOWN)) == 2000001
    assert hash(Variable(TypeVariable.UNKNOWN)) == 2000002
