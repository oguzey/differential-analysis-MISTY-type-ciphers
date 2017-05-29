from transition import Transition
from side import Side
from data.vars import *
from typing import Dict

cipher_name = 'test'   # type: str
systems = dict()        # type: Dict[int, System]

systems[3] = System(
    inputs=[a1, a2],
    outputs=[c1, c2],
    transitions=[Transition(Side(a1), Side(b1, cp_with_lo(a2, mu)), F),
                 Transition(Side(a2), Side(c2, cp_with_lo(b1, lmbda)), G),
                 Transition(Side(b1), Side(c1, cp_with_lo(c2, mu)), F)]
)