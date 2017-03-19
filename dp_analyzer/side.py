from variable import Variable
from variable import TypeVariable


class SideException(Exception):
    pass


class Side(object):
    def __init__(self, *args):
        assert all([isinstance(x, Variable) for x in args])
        self.__vars = list(args)

    def __eq__(self, other):
        if len(self.__vars) == len(other.__vars):
            for var in self.__vars:
                if var not in other.__vars:
                    return False
            return True
        return False

    def __str__(self):
        str_vars = map(lambda var: "[" + str(var) + "]", self.__vars)
        return " XOR ".join(str_vars) if len(str_vars) > 0 else "[]"

    def __len__(self):
        return len(self.__vars)

    def copy(self):
        return Side(*self.__vars)

    def equals(self, other):
        return self.__eq__(other)

    def contains(self, other):
        for var in other.__vars:
            if var not in self.__vars:
                return False
        return True

    def contains_element(self, element):
        return element in self.__vars

    def __contains_as_type(self, type_var):
        return any([var.is_as_type(type_var) for var in self.__vars])

    def contains_unknown(self):
        return self.__contains_as_type(TypeVariable.UNKNOWN)

    def contains_output(self):
        return self.__contains_as_type(TypeVariable.OUTPUT)

    def contains_intput(self):
        return self.__contains_as_type(TypeVariable.INPUT)

    def is_trivial(self):
        return all(map(lambda x: not x.is_unknown(), self.__vars))

    def is_empty(self):
        return len(self.__vars) == 0

    def get_vars(self):
        return self.__vars

    def get_unknowns_id(self):
        ids = []
        for var in self.__vars:
            if var.is_unknown():
                ids.append(var.get_id())
        return ids

    def __find_the_latest(self, type_var):
        if not self.__contains_as_type(type_var):
            raise SideException("No one %s Variable in Side" % str(type_var))
        max_var = None
        for var in self.__vars:
            if var.is_as_type(type_var):
                if max_var is None or var > max_var:
                    max_var = var

        assert max_var is not None
        return max_var

    def find_the_latest_unknown(self):
        return self.__find_the_latest(TypeVariable.UNKNOWN)

    def find_the_latest_output(self):
        return self.__find_the_latest(TypeVariable.OUTPUT)

    def find_the_latest_input(self):
        return self.__find_the_latest(TypeVariable.INPUT)

    def has_only_one_unknown(self):
        return len(self.__vars) == 1 and self.__vars[0].is_unknown()

    def pop_variable(self, var):
        length = len(self.__vars)
        assert self.contains_element(var)
        self.__vars.remove(var)
        assert len(self.__vars) == length - 1

    def __pop_all_by_type(self, type_var):
        elements = []
        for elem in self.__vars:
            if elem.is_as_type(type_var):
                elements.append(elem)

        for elem in elements:
            self.__vars.remove(elem)

        return elements

    def pop_all_unknowns(self):
        return self.__pop_all_by_type(TypeVariable.UNKNOWN)

    def replace_in_side(self, would_repl, replacement):
        """ all variables in 'would_repl' will be replaced to 'replacement' """
        assert isinstance(would_repl, Side) and isinstance(replacement, Side)
        assert self.contains(would_repl)
        # remove all elements from would_repl in self
        for var in would_repl.__vars:
            self.pop_variable(var)

        # add all elements from replacement to self
        self.add_side(replacement)

    def add_variable(self, variable):
        if self.contains_element(variable):
            self.pop_variable(variable)
        else:
            self.__vars.append(variable)

    def add_side(self, side):
        assert isinstance(side, Side)
        for var in side.__vars:
            self.add_variable(var)

    def move_side(self, other):
        while len(other.__vars) > 0:
            self.add_variable(other.__vars.pop(0))

    def get_the_latest_variable(self):
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
