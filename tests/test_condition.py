if __name__ == "__main__":
    import sys
    sys.path.append("dp_analyzer")
import pytest
from variable import Variable, TypeVariable
from conditions import CommonConditions
from logger import logger

def setup_module(module):
    global a1, a2, a3, a4
    a1 = Variable(TypeVariable.INPUT)
    a2 = Variable(TypeVariable.INPUT)
    a3 = Variable(TypeVariable.INPUT)
    a4 = Variable(TypeVariable.INPUT)
    
def test_generate_conditions():
    global a1, a2, a3, a4
    conds = CommonConditions(a1, a2, a3, a4)
    for index in range(len(conds)):
        logger.info("\t condition: {}".format(conds.get_condition(index)))
        
    assert len(conds) == 15


if __name__ == "__main__":
    setup_module(None)
    test_generate_conditions()
