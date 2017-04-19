from enum import Enum
from typing import Dict, List


class TypeVariable(Enum):
    INPUT = 0
    OUTPUT = 1
    UNKNOWN = 2

    def __str__(self):
        return self._name_.capitalize()


class Variable(object):
    # __k__ - coefficient for calculation hash of Variable
    __k__ = 1000000  # type: int
    __id__ = {
        TypeVariable.INPUT: 1,
        TypeVariable.OUTPUT: 1,
        TypeVariable.UNKNOWN: 1
    }  # type: Dict[Enum, int]
    instances = {
        TypeVariable.INPUT: [],
        TypeVariable.OUTPUT: [],
        TypeVariable.UNKNOWN: []
    }  # type: Dict[Enum, List[Variable]]

    def __init__(self, type_var: TypeVariable) -> None:
        super(Variable, self).__init__()
        Variable.instances[type_var].append(self)
        self.__id = Variable.__id__[type_var]  # type: int
        Variable.__id__[type_var] += 1
        self.__type = type_var  # type: TypeVariable
        self.__hash = Variable.__k__ * int(self.__type.value) + self.__id  # type: int

    def __eq__(self, other: 'Variable') -> bool:
        return self.__type == other.__type and self.__id == other.__id

    def __ne__(self, other: 'Variable') -> bool:
        return not self.__eq__(other)

    def __gt__(self, other: 'Variable') -> bool:
        if self.__type != other.__type:
            raise Exception("Compare two different types of Variables")
        return self.__id > other.__id

    def __str__(self) -> str:
        return "[{} : {}]".format(str(self.__type), self.__id)

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return self.__hash

    def is_unknown(self) -> bool:
        return self.__type == TypeVariable.UNKNOWN

    def is_input(self) -> bool:
        return self.__type == TypeVariable.INPUT

    def is_output(self) -> bool:
        return self.__type == TypeVariable.OUTPUT

    def has_type(self, type_var: TypeVariable) -> bool:
        return self.__type == type_var

    def get_id(self) -> int:
        return self.__id
