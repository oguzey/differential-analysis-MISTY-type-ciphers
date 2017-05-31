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
        self.__state = state  # type: ConditionState
        self.__left_side = left_side  # type: Side
        self.__right_side = right_side  # type: Side

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

    def normalise(self) -> bool:
        """
        Bring condition to particular format: a = b + c + ...
        Before call the function make sure that condition is not useless.
        """
        if self.__state == ConditionState.IS_NOT_ZERO:
            return False
        if len(self.__left_side) == 1 and len(self.__right_side) == 0 and self.__state == ConditionState.IS_ZERO:
            return False

        self.__right_side.merge_side(self.__left_side)
        var = self.__right_side.pop_the_latest_variable()
        if var:
            self.__left_side.add_variable(var)
            self.__right_side.move_lo_from_var(var)
        self.__state = ConditionState.IS_ZERO if self.__right_side.is_empty() else ConditionState.IS_EQUAL
        return True

    def update_with(self, condition: 'Condition') -> bool:
        if condition.__state == ConditionState.IS_NOT_ZERO:
            return True
        s = str(self)
        assert len(condition.__left_side) == 1 and len(condition.__right_side) <= 2
        res = False

        var = condition.__left_side.get_first()
        if self.__right_side.replace_var_by_side(var, condition.__right_side):
            res = True
        if self.__left_side.replace_var_by_side(var, condition.__right_side):
            res = True

        res2 = self.normalise()
        logger.debug("update_with {}: from {} to {}".format(condition, s, str(self)))
        return res or res2

    @staticmethod
    def create_zero_condition(side: Side) -> 'Condition':
        assert isinstance(side, Side) and not side.is_empty()
        s = str(side)
        var = side.pop_the_latest_variable()
        s_var = str(var)
        assert var is not None
        side.move_lo_from_var(var)
        c = Condition(Side(var), side, ConditionState.IS_ZERO if side.is_empty() else ConditionState.IS_EQUAL)
        logger.info("create_zero_condition: var: {}; side: {}. => '{}'".format(s_var, s, c))
        return c

    @staticmethod
    def create_non_zero_condition(side: Side) -> 'Condition':
        assert isinstance(side, Side) and not side.is_empty()
        return Condition(side, Side(), ConditionState.IS_NOT_ZERO)

    def check_contains_var(self, var: Variable, state: ConditionState):
        assert len(self.__left_side) == 1 and self.__right_side.is_empty()
        if self.__left_side.contains_element(var) and self.__state == state:
            return True
        return False
