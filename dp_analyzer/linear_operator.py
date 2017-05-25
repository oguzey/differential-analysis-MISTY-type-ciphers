from enum import Enum


class TypeLO(Enum):
    UNDEFINED = 0
    EXTENDER = 1
    CONSTRICTOR = 2

    def __str__(self):
        return self._name_.capitalize()


class LinearOperator(object):
    def __init__(self,  type_lo: TypeLO, name: str) -> None:
        self._type = type_lo
        self._name = name
        self._is_inverse = False

    def __str__(self) -> str:
        return self.get_name()

    def __eq__(self, other: 'LinearOperator') -> bool:
        return self._type == other._type and self._is_inverse == other._is_inverse

    def __ne__(self, other: 'LinearOperator') -> bool:
        return not self.__eq__(other)

    def get_type(self) -> TypeLO:
        return self._type

    def get_name(self) -> str:
        if self._is_inverse:
            return self._name + "^-1"
        else:
            return self._name

    def make_inverse(self) -> None:
        self._is_inverse = True

    def is_inverse(self) -> bool:
        return self._is_inverse

    def reset_inverse(self) -> None:
        self._is_inverse = False


class ExtenderLinearOperator(LinearOperator):
    def __init__(self) -> None:
        super(ExtenderLinearOperator,  self).__init__(TypeLO.EXTENDER,  "μ")

    def clone(self):
        c = ExtenderLinearOperator()
        c._is_inverse = self.is_inverse()
        return c


class ConstrictorLinearOperator(LinearOperator):
    def __init__(self) -> None:
        super(ConstrictorLinearOperator, self).__init__(TypeLO.CONSTRICTOR,  "λ")

    def clone(self):
        c = ConstrictorLinearOperator()
        c._is_inverse = self.is_inverse()
        return c

LOMu = ExtenderLinearOperator
LOLambda = ConstrictorLinearOperator