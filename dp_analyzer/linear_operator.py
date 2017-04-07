from enum import Enum

class TypeLO(Enum):
    UNDEFINED = 0
    EXTENDER = 1
    CONSTRICTOR = 2

    def __str__(self):
        return self._name_.capitalize()


class LinearOperator(object):
    def __init__(self,  type: TypeLO, name: str) -> None:
        self._type = type
        self._name = name
    
    def get_type(self) -> TypeLO:
        return self.__type
    
    def get_name(self) -> str:
        return self._name

class ExtenderLinearOperator(object):
    def __init__(self,  name: str) -> None:
        super(ExtenderLinearOperator,  self).__init__(TypeLO.EXTENDER,  name)
        
class ConstrictorLinearOperator(object):
    def __init__(self,  name):
        super(ConstrictorLinearOperator, self).__init__(TypeLO.CONSTRICTOR,  name)
