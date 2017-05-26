from variable import Variable, VariableType
from logger import logger
from typing import List, Union, Optional
from mypy_extensions import NoReturn


class SideException(Exception):
    pass


class Side(object):
    def __init__(self, *args: Variable) -> None:
        assert all([isinstance(x, Variable) for x in args])
        self.__vars = list(args)

    def __eq__(self, other: 'Side') -> bool:
        if len(self.__vars) != len(other.__vars):
            return False

        return sorted(self.__vars, key=hash) == sorted(other.__vars, key=hash)

    def __str__(self) -> str:
        return " ⊕ ".join(map(str, self.__vars)) if len(self.__vars) > 0 else "[]"

    def __len__(self) -> int:
        return len(self.__vars)

    def copy(self) -> 'Side':
        return Side(*[x.clone() for x in self.__vars])

    def equals(self, other: 'Side') -> bool:
        return self.__eq__(other)

    def contains(self, other: 'Side') -> bool:
        for var in other.__vars:
            if var not in self.__vars:
                return False
        return True

    def contains_element(self, element: Variable) -> bool:
        return element in self.__vars

    def __contains_as_type(self, type_var: VariableType) -> bool:
        return any([var.has_type(type_var) for var in self.__vars])

    def contains_unknown(self) -> bool:
        return self.__contains_as_type(VariableType.UNKNOWN)

    def contains_output(self) -> bool:
        return self.__contains_as_type(VariableType.OUTPUT)

    def contains_intput(self) -> bool:
        return self.__contains_as_type(VariableType.INPUT)

    def is_trivial(self) -> bool:
        return all(map(lambda x: not x.is_unknown(), self.__vars))

    def is_empty(self):
        return len(self.__vars) == 0

    def get_vars(self) -> List[Variable]:
        return self.__vars

    def get_unknowns_id(self) -> List[int]:
        ids = []
        for var in self.__vars:
            if var.is_unknown():
                ids.append(var.get_id())
        return ids

    def __find_the_latest(self, type_var: VariableType) -> Union[Variable, NoReturn]:
        max_var = None
        for var in self.__vars:
            if var.has_type(type_var):
                if max_var is None or var > max_var:
                    max_var = var

        if max_var is None:
            raise SideException("No one %s Variable in Side" % str(type_var))
        return max_var

    def find_the_latest_unknown(self) -> Union[Variable, NoReturn]:
        return self.__find_the_latest(VariableType.UNKNOWN)

    def find_the_latest_output(self) -> Union[Variable, NoReturn]:
        return self.__find_the_latest(VariableType.OUTPUT)

    def find_the_latest_input(self) -> Union[Variable, NoReturn]:
        return self.__find_the_latest(VariableType.INPUT)

    def has_only_one_unknown(self) -> bool:
        return len(self.__vars) == 1 and self.__vars[0].is_unknown()

    def pop_variable(self, var: Variable) -> None:
        self.__vars.remove(var)

    def pop_first_variable(self) -> Optional[Variable]:
        if len(self.__vars):
            return self.__vars.pop(0)
        else:
            return None

    def __pop_all_by_type(self, type_var: VariableType) -> List[Variable]:
        elements = []
        for elem in self.__vars:
            if elem.has_type(type_var):
                elements.append(elem)

        for elem in elements:
            self.__vars.remove(elem)

        return elements

    def pop_all_unknowns(self) -> List[Variable]:
        return self.__pop_all_by_type(VariableType.UNKNOWN)

    def replace_in_side(self, would_repl: 'Side', replacement: 'Side') -> None:
        """ all variables in 'would_repl' will be replaced to 'replacement' """
        assert isinstance(would_repl, Side) and isinstance(replacement, Side)
        assert self.contains(would_repl)
        # remove all elements from would_repl in self
        for var in would_repl.__vars:
            self.pop_variable(var)

        # add all elements from replacement to self
        self.add_side(replacement)

    def add_variable(self, variable: Optional[Variable]) -> None:
        if variable is None:
            return
        if self.contains_element(variable):
            self.pop_variable(variable)
        else:
            self.__vars.append(variable)

    def add_side(self, side: 'Side') -> None:
        assert isinstance(side, Side)
        for var in side.__vars:
            self.add_variable(var)

    def merge_side(self, other: 'Side') -> None:
        while len(other.__vars) > 0:
            self.add_variable(other.__vars.pop(0))

    def pop_the_latest_variable(self) -> Variable:
        length = len(self.__vars)
        if length == 0:
            return None
        if length == 1:
            return self.__vars.pop(0)
        try:
            lat_unknown = self.find_the_latest_unknown()
            self.pop_variable(lat_unknown)
            return lat_unknown
        except SideException:
            try:
                lat_output = self.find_the_latest_output()
                self.pop_variable(lat_output)
                return lat_output
            except SideException:
                lat_input = self.find_the_latest_input()
                self.pop_variable(lat_input)
                return lat_input
