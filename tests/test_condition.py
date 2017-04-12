if __name__ == "__main__":
    import sys
    sys.path.append("dp_analyzer")
import pytest
from variable import Variable, TypeVariable
from common_condition_generator import CommonConditionGenerator
from analyzer import zero_conds_to_str, non_zero_conds_to_str
from logger import logger


def setup_module(module):
    global a1, a2, a3, a4
    a1 = Variable(TypeVariable.INPUT)
    a2 = Variable(TypeVariable.INPUT)
    a3 = Variable(TypeVariable.INPUT)
    a4 = Variable(TypeVariable.INPUT)


def test_generate_conditions():
    global a1, a2, a3, a4
    ccg = CommonConditionGenerator()
    conds = ccg.gen_all_common_conditions([a1, a2, a3, a4])
    assert len(conds) == 15  # 2^4 -1

    for zero_conds, non_zero_conds in conds:
        logger.info(zero_conds_to_str(zero_conds))
        logger.info(non_zero_conds_to_str(non_zero_conds))


if __name__ == "__main__":
    setup_module(None)
    test_generate_conditions()
