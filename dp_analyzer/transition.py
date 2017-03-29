from side import Side
from conditions import Condition
from conditions import StateConditions
from conditions import ConditionException
from logger import logger


class Transition(object):
    def __init__(self, left_side, right_side):
        assert isinstance(left_side, Side) and isinstance(right_side, Side)
        self.__left = left_side
        self.__right = right_side
        # test property, need to review
        self.__is_simple = False

    def __str__(self):
        return "{} ---> {}".format(str(self.__left), str(self.__right))

    def set_simple(self):
        self.__is_simple = True

    def get_simple(self):
        return self.__is_simple

    def check_triviality(self):
        return self.__left.is_trivial() and self.__right.is_trivial()

    def copy(self):
        return Transition(self.__left.copy(), self.__right.copy())

    def apply_condition(self, condition):
        if condition.get_state() == StateConditions.IS_NOT_ZERO:
            return

        condition_left = condition.get_left_side()
        condition_right = condition.get_right_side()
        # if self.__left.contains(condition_left) and (
        #         not condition_right.contains_unknown() or
        #         len(condition_right) == 1):
        if self.__left.contains(condition_left):
            self.__left.replace_in_side(condition_left, condition_right)

        if self.__right.contains(condition_left):
            self.__right.replace_in_side(condition_left, condition_right)

    def has_empty_side(self):
        return self.__left.is_empty() or self.__right.is_empty()

    def has_both_empty_side(self):
        return self.__left.is_empty() and self.__right.is_empty()

    def get_left_side(self):
        return self.__left

    def get_right_side(self):
        return self.__right

    def make_condition(self):

        if self.__left.is_empty() and not self.__right.is_empty():
            non_zero_side = self.__right
        elif not self.__left.is_empty() and self.__right.is_empty():
            non_zero_side = self.__left
        else:
            raise Exception("One side must be not empty in transition")

        return Condition.create_zero_condition(non_zero_side)
