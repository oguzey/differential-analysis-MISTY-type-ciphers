from transition import Transition
from side import Side
from data.vars import *
from typing import Dict

cipher_name = 'skipjack'   # type: str
systems = dict()        # type: Dict[int, System]

systems[3] = System(
    inputs=[a1, a2, a3],
    outputs=[c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(c2), F),
        Transition(Side(a2, cp_and_use_lo(c2, lmbda)), Side(c3), G),
        Transition(Side(a3, cp_and_use_lo(c3, mu)), Side(c4), F)
    ]
)  # c1 = a4 + lambda(c4)

systems[4] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(c1, cp_and_use_lo(c4, mu)), F),                                                       #  Transition(Side(a1), Side(b1), F),
        Transition(Side(a2, cp_and_use_lo(c1, lmbda), cp_and_use_lo(c4, mu, lmbda)), Side(c2), G),                      #  Transition(Side(a2, cp_and_use_lo(b1, lmbda)), Side(c2), G),
        Transition(Side(a3, cp_and_use_lo(c2, mu)), Side(c3), F),
        Transition(Side(a4, cp_and_use_lo(c3, lmbda)), Side(c4), G)
    ]
)  # b1 = c1 + mu(c4)

systems[5] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1), F),
        Transition(Side(a2, cp_and_use_lo(b1, lmbda)), Side(c1, cp_and_use_lo(c4, lmbda)), G),                          # Transition(Side(a2, cp_and_use_lo(b1, lmbda)), Side(b2), G)
        Transition(Side(a3, cp_and_use_lo(c1, mu), cp_and_use_lo(c4, lmbda, mu)), Side(c2), F),                         # Transition(Side(a3, cp_and_use_lo(b2, mu)), Side(c2), F),
        Transition(Side(a4, cp_and_use_lo(c2, lmbda)), Side(c3), G),
        Transition(Side(b1, cp_and_use_lo(c3, mu)), Side(c4), F)
    ]
)  # b2 = c1 + lambda(c4)
