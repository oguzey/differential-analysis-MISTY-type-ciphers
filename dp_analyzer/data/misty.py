from transition import Transition
from side import Side
from data.vars import *
from typing import Dict

cipher_name = 'misty'   # type: str
systems = dict()        # type: Dict[int, System]

systems[3] = System(
    inputs=[a1, a2],
    outputs=[c1, c2],
    transitions=[Transition(Side(a1), Side(b1, clone_with_use_oper(a2, mu)), F),
                 Transition(Side(a2), Side(c2, clone_with_use_oper(b1, lmbda)), G),
                 Transition(Side(b1), Side(c1, clone_with_use_oper(c2, mu)), F)]
)
