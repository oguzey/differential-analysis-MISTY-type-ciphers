from enum import Enum
from typing import Dict, List, Union, Optional
from linear_operator import LOLambda, LOMu


class VariableType(Enum):
    INPUT = 0
    OUTPUT = 1
    UNKNOWN = 2
    ZERO = 3

    def __str__(self):
        return {VariableType.INPUT: 'a',
                VariableType.OUTPUT: 'c',
                VariableType.UNKNOWN: 'b',
                VariableType.ZERO: '0'}.get(self, None)


class Variable(object):
    # __k__ - coefficient for calculation hash of Variable
    __k__ = 1000000000  # type: int
    __id__ = {
        VariableType.INPUT: 1,
        VariableType.OUTPUT: 1,
        VariableType.UNKNOWN: 1,
        VariableType.ZERO: 1
    }  # type: Dict[Enum, int]
    instances = {
        VariableType.INPUT: [],
        VariableType.OUTPUT: [],
        VariableType.UNKNOWN: [],
        VariableType.ZERO: []
    }  # type: Dict[Enum, List[Variable]]

    def __init__(self, type_var: VariableType, id: int=None) -> None:
        super(Variable, self).__init__()
        Variable.instances[type_var].append(self)
        if id is not None:
            self.__id = id
        else:
            self.__id = Variable.__id__[type_var]  # type: int
        # TODO: make it thread save
        Variable.__id__[type_var] += 1
        self.__type = type_var  # type: VariableType
        self.__hash = Variable.__k__ * int(self.__type.value) + self.__id  # type: int
        self.__loperators = []  # type: List[Union[LOLambda, LOMu]]

    def __eq__(self, other: 'Variable') -> bool:
        if not (self.__type == other.__type and self.__id == other.__id):
            return False
        elif len(self.__loperators) != len(other.__loperators):
            return False
        else:
            for index in range(len(self.__loperators)):
                if self.__loperators[index] != other.__loperators[index]:
                    return False
            return True

    def __ne__(self, other: 'Variable') -> bool:
        return not self.__eq__(other)

    def __gt__(self, other: 'Variable') -> bool:
        if self.__type != other.__type:
            raise Exception("Compare two different types of Variables")
        return self.__id > other.__id

    def __str__(self) -> str:
        res = "{}{}".format(str(self.__type), self.__id)
        for lop in self.__loperators:
            res = "{}({})".format(lop.get_name(), res)
        return res

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return self.__hash

    def is_unknown(self) -> bool:
        return self.__type == VariableType.UNKNOWN

    def is_input(self) -> bool:
        return self.__type == VariableType.INPUT

    def is_output(self) -> bool:
        return self.__type == VariableType.OUTPUT

    def has_type(self, type_var: VariableType) -> bool:
        return self.__type == type_var

    def get_id(self) -> int:
        return self.__id

    def clone(self) -> 'Variable':
        #  XXX: Variable.__id will be increasing
        x = Variable(self.__type, self.__id)
        for lop in self.__loperators:
            x.apply_lin_oper(lop.clone())
        return x

    def apply_lin_oper(self, lin_op: Union[LOMu, LOLambda]):
        assert lin_op is not None
        self.__loperators.append(lin_op)

    def move_operators(self, other: Optional['Variable']) -> 'Variable':
        while len(self.__loperators):
            l = self.__loperators.pop(0)
            l.make_inverse()
            if other is None:
                # create ZERO variable as
                # LOLambda^-1(0) == N
                if isinstance(l, LOLambda) and l.is_inverse() == True:
                    other = Variable(VariableType.ZERO)
                else:
                    # in all other cases we have zero result
                    # mu(0) = 0;  mu^-1(0) = 0; lambda(0) = 0
                    continue
                other.__loperators.append(l)
        return other
