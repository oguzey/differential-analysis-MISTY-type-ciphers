if __name__ == "__main__":
    import sys
    sys.path.append("dp_analyzer")
import pytest
from variable import Variable, VariableType
from common_condition_generator import CommonConditionGenerator
from analyzer import zero_conds_to_str, non_zero_conds_to_str
from condition import Condition, ConditionState
from side import Side
from logger import logger


def setup_module(module):
    global a1, a2, a3, a4
    a1 = Variable(VariableType.INPUT)
    a2 = Variable(VariableType.INPUT)
    a3 = Variable(VariableType.INPUT)
    a4 = Variable(VariableType.INPUT)


def test_generate_conditions():
    global a1, a2, a3, a4
    ccg = CommonConditionGenerator()
    conds = ccg.gen_all_common_conditions([a1, a2, a3, a4])
    assert len(conds) == 15  # 2^4 -1

    for zero_conds, non_zero_conds in conds:
        logger.info(zero_conds_to_str(zero_conds))
        logger.info(non_zero_conds_to_str(non_zero_conds))


def test_to_srt():
    global a1, a2, a3
    assert "{} = {}".format(a1, a2) == str(Condition(Side(a1), Side(a2), ConditionState.IS_EQUAL))
    assert "{} != 0".format(a1) == str(Condition(Side(a1), Side(), ConditionState.IS_NOT_ZERO))
    assert "{} != {}".format(a1, a2) == str(Condition(Side(a1), Side(a2), ConditionState.IS_NOT_ZERO))
    assert "{} = 0".format(a1) == str(Condition(Side(a1), Side(), ConditionState.IS_ZERO))

if __name__ == "__main__":
    setup_module(None)
    test_generate_conditions()
