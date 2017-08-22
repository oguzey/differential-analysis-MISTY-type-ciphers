from typing import List, Tuple
from functools import cmp_to_key
from variable import Variable
from side import Side
from condition import Condition, ConditionState


class CommonConditionGenerator(object):
    """
    Generates all possible combination of zero conditions and non zero conditions
    for determined input or output variables
    """
    def __init__(self) -> None:
        pass

    @staticmethod
    def __get_num_bits(number: int, max_bits: int) -> List[int]:
        res = []
        counter, comp = 0, 1
        while counter < max_bits:
            if (comp & number) > 0:
                res.append(counter)
            counter += 1
            comp *= 2
        return res

    @staticmethod
    def __comparator(lst1: List[int], lst2: List[int]) -> int:
        if len(lst1) < len(lst2):
            return -1
        elif len(lst1) > len(lst2):
            return 1
        else:
            return 1 if lst1 > lst2 else -1

    def __generate_zero_positions(self, input_variables: List[Variable]) -> List[List[int]]:
        max_bits = len(input_variables)
        max_number = pow(2, max_bits)
        zero_pos = []

        for x in range(1, max_number - 1):
            zero_pos.append(self.__get_num_bits(x, max_bits))
        zero_pos.sort(key=cmp_to_key(self.__comparator))
        zero_pos.append([])
        return zero_pos

    def gen_all_common_conditions(self, variables: List[Variable]) -> List[Tuple[List[Condition], List[Condition]]]:
        assert all([isinstance(x, Variable) and not x.is_unknown() for x in variables])
        cconditions = []  # type: List[Tuple[List[Condition], List[Condition]]]

        assert len(variables) > 0

        for zero_pos in self.__generate_zero_positions(variables):
            zero_conds = []  # type: List[Condition]
            none_zero_conds = []  # type: List[Condition]
            for index in range(len(variables)):
                if index in zero_pos:
                    zero_conds.append(Condition(Side(variables[index]), Side(), ConditionState.IS_ZERO))
                else:
                    none_zero_conds.append(Condition(Side(variables[index]), Side(), ConditionState.IS_NOT_ZERO))
            cconditions.append((zero_conds, none_zero_conds))
        return cconditions