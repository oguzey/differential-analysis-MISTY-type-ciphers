from enum import Enum
from variable import Variable
from side import Side
from logger import logger
from typing import List, Tuple, Union, Optional
from mypy_extensions import NoReturn


class ConditionException(Exception):
    pass


class StateConditions(Enum):
    IS_ZERO = 0
    IS_NOT_ZERO = 1
    IS_EQUAL = 2
    
    def __str__(self) -> str:
        return {
            StateConditions.IS_ZERO: '=',
            StateConditions.IS_NOT_ZERO: '!=',
            StateConditions.IS_EQUAL: '='
        }.get(self, '')


class CompareCondition(Enum):
    CONTRADICTION = 0
    NOT_EQUAL = 1
    EQUAL = 2


class Condition(object):
    """ Describes conditions for system of transitions"""
    def __init__(self, left_side: Side, right_side: Side, state: StateConditions) -> None:
        """
        left_side - is list of Variables
        left_side - is list of Variables or None if state equal IS_ZERO
        state - state of condition
        """
        if not right_side.is_empty() and state == StateConditions.IS_ZERO:
            assert "Internal error" == 0
        self.__state = state
        self.__left_side = left_side
        self.__right_side = right_side

    def __eq__(self, other: 'Condition') -> bool:
        return self.__state == other.__state and (
            self.__left_side == other.__left_side and (
                self.__right_side == other.__right_side))

    def __str__(self) -> str:
        assert not self.__left_side.is_empty()
        rside = '0' if self.__right_side.is_empty() else str(self.__right_side)
        return '{} {} {}'.format(self.__left_side, self.__state, rside)

    def get_left_side(self) -> Side:
        return self.__left_side

    def get_right_side(self) -> Side:
        return self.__right_side

    def get_state(self) -> StateConditions:
        return self.__state

    def set_state(self, state: StateConditions) -> None:
        self.__state = state

    def copy(self) -> 'Condition':
        return Condition(self.__left_side.copy(), self.__right_side.copy(), self.__state)

    def is_correct(self) -> bool:
        if self.__right_side.is_empty():
            if self.__state == StateConditions.IS_EQUAL:
                return False
            if self.__left_side.is_empty() and self.__state == StateConditions.IS_NOT_ZERO:
                return False
        else:
            # TODO: check me
            if self.__state != StateConditions.IS_EQUAL:
                return False
        # TODO: check case (EMPTY, EMPTY, IS_ZERO)
        if self.__left_side == self.__right_side and self.__state != StateConditions.IS_EQUAL:
            return False
        return True

    def is_useless(self) -> bool:
        if self.__left_side.is_empty() and self.__right_side.is_empty() and (
                self.__state == StateConditions.IS_ZERO or self.__state == StateConditions.IS_EQUAL):
            return True
        if self.__left_side == self.__right_side and self.__state == StateConditions.IS_EQUAL:
            return True
        return False

    def swap_sides(self) -> None:
        new_left_side = self.__right_side
        self.__right_side = self.__left_side
        self.__left_side = new_left_side

    def normalise(self) -> None:
        """
        Bring condition to particular format: a = b + c + ...
        Before call the function make sure that condition is not useless.
        """
        if self.__state == StateConditions.IS_NOT_ZERO:
            return
        # FIXME: it is possible case that [0(left)] IS_EQUAL [a1, ... (rigth)]
        self.__right_side.merge_side(self.__left_side)
        var = self.__right_side.pop_the_latest_variable()
        if var:
            self.__left_side.add_variable(var)
        self.__state = StateConditions.IS_ZERO if self.__right_side.is_empty() else StateConditions.IS_EQUAL

    def update_with(self, condition: 'Condition') -> None:
        if condition.__state == StateConditions.IS_NOT_ZERO:
            return

        if self.__right_side.contains(condition.__left_side):
            self.__right_side.replace_in_side(condition.__left_side, condition.__right_side)
        if self.__left_side.contains(condition.__left_side):
            self.__left_side.replace_in_side(condition.__left_side, condition.__right_side)

        self.normalise()

    def __get_all_in_left_side(self) -> Tuple[Side, StateConditions]:
        if self.__state == StateConditions.IS_NOT_ZERO:
            return self.__left_side, self.__state
        else:
            c = self.__right_side.copy()
            c.add_side(self.__left_side)
            return c, StateConditions.IS_ZERO

    def compare_conditions(self, other: 'Condition') -> CompareCondition:
        """
        can return
            CompareCondition.EQUAL
            CompareCondition.CONTRADICTION
            CompareCondition.NOT_EQUAL
        """
        assert isinstance(other, Condition)
        if not self.is_correct() or not other.is_correct():
            return CompareCondition.CONTRADICTION
        side_self, state_self = self.__get_all_in_left_side()
        side_other, state_other = other.__get_all_in_left_side()
        # logger.debug("[compare_conditions] %s vs %s" % (str(self), str(other))
        if side_self == side_other:
            return CompareCondition.EQUAL if state_self == state_other else CompareCondition.CONTRADICTION
        else:
            return CompareCondition.NOT_EQUAL

    @staticmethod
    def create_zero_condition(side: Side) -> 'Condition':
        assert isinstance(side, Side) and not side.is_empty()
        var = side.pop_the_latest_variable()
        return Condition(Side(var), side, StateConditions.IS_ZERO if side.is_empty() else StateConditions.IS_EQUAL)

    @staticmethod
    def create_non_zero_condition(side: Side) -> 'Condition':
        assert isinstance(side, Side) and not side.is_empty()
        return Condition(side, Side(), StateConditions.IS_NOT_ZERO)


# class CustomConditions(object):
#     """
#     conditions which is created during applying CommonConditions and assumption
#     """
#     def __init__(self) -> None:
#         self.__conditions = []  # type: List[Condition]
#
#     def __str__(self) -> str:
#         str_cc = "\n\t".join(map(str, self.__conditions))
#         return "{ \n\t" + str_cc + " \n}"
#
#     def __len__(self) -> int:
#         return len(self.__conditions)
#
#     def __is_exist_conditions(self, cond: Condition) -> bool:
#         for condition in self.__conditions:
#             if cond == condition:
#                 return True
#         return False
#
#     def __update_all(self) -> Union[NoReturn, None]:
#         length = len(self.__conditions)
#         for x in range(length):
#             first = self.__conditions[x]
#             for y in range(length):
#                 if x != y:
#                     second = self.__conditions[y]
#                     second.update_with(first)
#                     if not second.is_correct():
#                         raise ConditionException("Bad condition %s" % str(second))
#
#     def __update_conditions(self) -> None:
#         self.__update_all()
#         # logger.debug("[append_condition] after __update_all " + str(self)
#         self.remove_duplicate_conditions()
#         # logger.debug("[append_condition] after remove_duplicate_conditions " + str(self)
#         if self.exist_contradiction_internal():
#             raise ConditionException("contains contradictions")
#         # logger.debug("[append_condition] after exist_contradiction " + str(self)
#         self.remove_useless()
#
#     def append_condition(self, condition: Condition) -> None:
#         logger.debug("[append_condition] append " + str(condition))
#         # logger.debug("[append_condition] to " + str(self)
#         if not self.__is_exist_conditions(condition):
#             self.__conditions.append(condition)
#         # logger.debug("[append_condition] after append " + str(self)
#         self.__update_conditions()
#         logger.debug("[append_condition] cc became " + str(self))
#
#     def remove_duplicate_conditions(self) -> None:
#         rm = []
#         length = len(self.__conditions)
#         for x in range(length):
#             first = self.__conditions[x]
#             for y in range(x + 1, length):
#                 second = self.__conditions[y]
#                 if first.compare_conditions(second) == CompareCondition.EQUAL:
#                     rm.append(second)
#
#         for cond in rm:
#             logger.debug("[remove_duplicate_conditions] will remove " + str(cond))
#             self.__conditions.remove(cond)
#
#     def remove_useless(self) -> None:
#         rm = []
#         for cond in self.__conditions:
#             if cond.is_useless():
#                 rm.append(cond)
#         for cond in rm:
#             logger.debug("[remove_useless] will remove " + str(cond))
#             self.__conditions.remove(cond)
#
#     def get_condition(self, index: int) -> 'Condition':
#         assert index <= len(self.__conditions)
#         return self.__conditions[index]
#
#     def exist_contradiction(self, common_conditions: List[Condition]) -> bool:
#         assert isinstance(common_conditions, list)
#
#         for self_cond in self.__conditions:
#             for c in common_conditions:
#                 if c.compare_conditions(self_cond) == CompareCondition.CONTRADICTION:
#                     logger.debug("Found contradictions %s and %s" % (str(c), str(self_cond)))
#                     return True
#         logger.debug("Contradiction not found with common_conditions")
#         return self.exist_contradiction_internal()
#
#     def exist_contradiction_internal(self) -> bool:
#         length = len(self.__conditions)
#         for x in range(length):
#             first = self.__conditions[x]
#             for y in range(x + 1, length):
#                 second = self.__conditions[y]
#                 if first.compare_conditions(second) == CompareCondition.CONTRADICTION:
#                     logger.debug("Found contradictions %s and %s" % (str(first), str(second)))
#                     return True
#         logger.debug("Contradictions not found")
#         return False
#
#     def copy(self) -> 'CustomConditions':
#         new_cc = CustomConditions()
#         for condition in self.__conditions:
#             new_cc.__conditions.append(condition.copy())
#             # new_cc.append_condition(condition.copy())
#         new_cc.__update_conditions()
#
#         return new_cc
#
#     def is_side_non_zero(self, side: Side, additional_conditions: Optional[List[Condition]]=None) -> bool:
#         for condition in self.__conditions:
#             if condition.get_state() == StateConditions.IS_NOT_ZERO and (
#                     condition.get_left_side() == side):
#                 return True
#         if additional_conditions is None:
#             return False
#
#         for condition in additional_conditions:
#             assert condition.get_state() == StateConditions.IS_NOT_ZERO
#             if condition.get_left_side() == side:
#                 return True
#         return False
