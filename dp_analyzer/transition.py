from side import Side
from condition import Condition
from condition import ConditionState
from typing import Union
from mypy_extensions import NoReturn
from logger import logger


class BlockFunction(object):
    def __init__(self, name: str, sign_probability: str) -> None:
        self._name = name
        self._sign_prob = sign_probability

    def __repr__(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self._name

    def get_probability(self) -> str:
        return self._sign_prob


class Transition(object):
    def __init__(self, left_side: Side, right_side: Side, block_function: BlockFunction) -> None:
        self.__left = left_side
        self.__right = right_side
        # TODO: test property, need to review
        self.__is_simple = False
        self._block_func = block_function

    def __str__(self) -> str:
        return "{} --{}--> {}".format(str(self.__left), self._block_func, str(self.__right))

    def get_probability(self) -> str:
        return self._block_func.get_probability()

    def get_left_side(self) -> Side:
        return self.__left

    def get_right_side(self) -> Side:
        return self.__right

    def make_simple(self) -> None:
        self.__is_simple = True

    def check_triviality(self) -> bool:
        return self.__left.is_trivial() and self.__right.is_trivial()

    def copy(self) -> 'Transition':
        return Transition(self.__left.copy(), self.__right.copy(), self._block_func)

    def apply_condition(self, condition: Condition) -> None:
        """
        Apply the condition to this transition
        :param condition: Condition should be already formatted! i.e. format should be like A = B + C
        :return: None
        """
        if condition.get_state() == ConditionState.IS_NOT_ZERO:
            logger.warn("Can not apply NOT_ZERO condition: {}".format(condition))
            return

        condition_left = condition.get_left_side()
        condition_right = condition.get_right_side()

        # XXX: Expect formatted condition
        assert len(condition_left) == 1
        var = condition_left.get_first()

        self.__left.replace_var_by_side(var, condition_right)
        self.__right.replace_var_by_side(var, condition_right)

    def has_empty_side(self) -> bool:
        return self.__left.is_empty() or self.__right.is_empty()

    def has_both_empty_side(self) -> bool:
        return self.__left.is_empty() and self.__right.is_empty()

    def make_zero_condition(self) -> Union[Condition, NoReturn]:

        if self.__left.is_empty() and not self.__right.is_empty():
            non_zero_side = self.__right
        elif not self.__left.is_empty() and self.__right.is_empty():
            non_zero_side = self.__left
        else:
            raise Exception("One side must be not empty in transition")

        return Condition.create_zero_condition(non_zero_side)
