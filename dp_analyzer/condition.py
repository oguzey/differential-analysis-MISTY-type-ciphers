from enum import Enum
from variable import Variable
from side import Side
from logger import logger
from typing import List, Tuple, Union, Optional
from mypy_extensions import NoReturn


class ConditionException(Exception):
    pass


class ConditionState(Enum):
    IS_ZERO = 0
    IS_NOT_ZERO = 1
    IS_EQUAL = 2
    
    def __str__(self) -> str:
        return {
            ConditionState.IS_ZERO: '=',
            ConditionState.IS_NOT_ZERO: '!=',
            ConditionState.IS_EQUAL: '='
        }.get(self, '')


class CompareCondition(Enum):
    CONTRADICTION = 0
    NOT_EQUAL = 1
    EQUAL = 2


class Condition(object):
    """ Describes conditions for system of transitions"""
    def __init__(self, left_side: Side, right_side: Side, state: ConditionState) -> None:
        """
        left_side - is list of Variables
        left_side - is list of Variables or None if state equal IS_ZERO
        state - state of condition
        """
        if not right_side.is_empty() and state == ConditionState.IS_ZERO:
            assert "Internal error" == 0
        self.__state = state
        self.__left_side = left_side
        self.__right_side = right_side

    def __eq__(self, other: 'Condition') -> bool:
        return self.__state == other.__state and (
            self.__left_side == other.__left_side and (
                self.__right_side == other.__right_side))

    def __str__(self) -> str:
        # assert not self.__left_side.is_empty()
        rside = '0' if self.__right_side.is_empty() else str(self.__right_side)
        return '{} {} {}'.format(self.__left_side, self.__state, rside)

    def get_left_side(self) -> Side:
        return self.__left_side

    def get_right_side(self) -> Side:
        return self.__right_side

    def get_state(self) -> ConditionState:
        return self.__state

    def set_state(self, state: ConditionState) -> None:
        self.__state = state

    def copy(self) -> 'Condition':
        return Condition(self.__left_side.copy(), self.__right_side.copy(), self.__state)

    def is_correct(self) -> bool:
        if self.__right_side.is_empty():
            if self.__state == ConditionState.IS_EQUAL:
                return False
            if self.__left_side.is_empty() and self.__state == ConditionState.IS_NOT_ZERO:
                return False
        else:
            # TODO: check me
            if self.__state != ConditionState.IS_EQUAL:
                return False
        # TODO: check case (EMPTY, EMPTY, IS_ZERO)
        if self.__left_side == self.__right_side and self.__state != ConditionState.IS_EQUAL:
            return False
        return True

    def is_useless(self) -> bool:
        if self.__left_side.is_empty() and self.__right_side.is_empty() and (
                self.__state == ConditionState.IS_ZERO or self.__state == ConditionState.IS_EQUAL):
            return True
        if self.__left_side == self.__right_side and self.__state == ConditionState.IS_EQUAL:
            return True
        return False

    def swap_sides(self) -> None:
        new_left_side = self.__right_side
        self.__right_side = self.__left_side
        self.__left_side = new_left_side

    def normalise(self) -> bool:
        """
        Bring condition to particular format: a = b + c + ...
        Before call the function make sure that condition is not useless.
        """
        if self.__state == ConditionState.IS_NOT_ZERO:
            return False
        if len(self.__left_side) == 1 and len(self.__right_side) == 0 and self.__state == ConditionState.IS_ZERO:
            return False
        # FIXME: it is possible case that [0(left)] IS_EQUAL [a1, ... (rigth)]
        self.__right_side.merge_side(self.__left_side)
        var = self.__right_side.pop_the_latest_variable()
        if var:
            self.__left_side.add_variable(var)
        self.__state = ConditionState.IS_ZERO if self.__right_side.is_empty() else ConditionState.IS_EQUAL
        return True

    def update_with(self, condition: 'Condition') -> bool:
        if condition.__state == ConditionState.IS_NOT_ZERO:
            return True

        res = False
        if self.__right_side.contains(condition.__left_side):
            self.__right_side.replace_in_side(condition.__left_side, condition.__right_side)
            res = True
        if self.__left_side.contains(condition.__left_side):
            self.__left_side.replace_in_side(condition.__left_side, condition.__right_side)
            res = True

        res2 = self.normalise()
        return res or res2

    def __get_all_in_left_side(self) -> Tuple[Side, ConditionState]:
        if self.__state == ConditionState.IS_NOT_ZERO:
            return self.__left_side, self.__state
        else:
            c = self.__right_side.copy()
            c.add_side(self.__left_side)
            return c, ConditionState.IS_ZERO

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
        return Condition(Side(var), side, ConditionState.IS_ZERO if side.is_empty() else ConditionState.IS_EQUAL)

    @staticmethod
    def create_non_zero_condition(side: Side) -> 'Condition':
        assert isinstance(side, Side) and not side.is_empty()
        return Condition(side, Side(), ConditionState.IS_NOT_ZERO)