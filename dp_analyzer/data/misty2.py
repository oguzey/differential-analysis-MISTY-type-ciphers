from transition import Transition
from side import Side
from data.vars import *
from typing import Dict

cipher_name = 'misty2'   # type: str
systems = dict()         # type: Dict[int, System]

systems[2] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(c3, cp_with_lo(a2, mu)), F),
        Transition(Side(a3), Side(c1, cp_with_lo(a4, mu)), F),

        Transition(Side(a2), Side(c4, cp_with_lo(c1, lmbda)), G),
        Transition(Side(a4), Side(c2, cp_with_lo(c3, lmbda)), G)
    ]
)

systems[3] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b2, cp_with_lo(a2, mu)), F),
        Transition(Side(a3), Side(b1, cp_with_lo(a4, mu)), F),

        Transition(Side(a2), Side(c3, cp_with_lo(b1, lmbda)), G),
        Transition(Side(a4), Side(c1, cp_with_lo(b2, lmbda)), G),

        Transition(Side(b1), Side(c4, cp_with_lo(c1, mu)), F),
        Transition(Side(b2), Side(c2, cp_with_lo(c3, mu)), F)
    ]
)

systems[4] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b2, cp_with_lo(a2, mu)), F),
        Transition(Side(a3), Side(b1, cp_with_lo(a4, mu)), F),

        Transition(Side(a2), Side(b4, cp_with_lo(b1, lmbda)), G),
        Transition(Side(a4), Side(b3, cp_with_lo(b2, lmbda)), G),

        Transition(Side(b1), Side(c3, cp_with_lo(b3, mu)), F),
        Transition(Side(b2), Side(c1, cp_with_lo(b4, mu)), F),

        Transition(Side(b3), Side(c4, cp_with_lo(c1, lmbda)), G),
        Transition(Side(b4), Side(c2, cp_with_lo(c3, lmbda)), G)
    ]
)

systems[5] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b2, cp_with_lo(a2, mu)), F),
        Transition(Side(a3), Side(b1, cp_with_lo(a4, mu)), F),

        Transition(Side(a2), Side(b4, cp_with_lo(b1, lmbda)), G),
        Transition(Side(a4), Side(b3, cp_with_lo(b2, lmbda)), G),

        Transition(Side(b1), Side(b6, cp_with_lo(b3, mu)), F),
        Transition(Side(b2), Side(b5, cp_with_lo(b4, mu)), F),

        Transition(Side(b3), Side(c3, cp_with_lo(b5, lmbda)), G),
        Transition(Side(b4), Side(c1, cp_with_lo(b6, lmbda)), G),

        Transition(Side(b5), Side(c4, cp_with_lo(c1, mu)), F),
        Transition(Side(b6), Side(c2, cp_with_lo(c3, mu)), F)
    ]
)

systems[6] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b2, cp_with_lo(a2, mu)), F),
        Transition(Side(a3), Side(b1, cp_with_lo(a4, mu)), F),

        Transition(Side(a2), Side(b4, cp_with_lo(b1, lmbda)), G),
        Transition(Side(a4), Side(b3, cp_with_lo(b2, lmbda)), G),

        Transition(Side(b1), Side(b6, cp_with_lo(b3, mu)), F),
        Transition(Side(b2), Side(b5, cp_with_lo(b4, mu)), F),

        Transition(Side(b3), Side(b8, cp_with_lo(b5, lmbda)), G),
        Transition(Side(b4), Side(b7, cp_with_lo(b6, lmbda)), G),

        Transition(Side(b5), Side(c3, cp_with_lo(b7, mu)), F),
        Transition(Side(b6), Side(c1, cp_with_lo(b8, mu)), F),

        Transition(Side(b7), Side(c4, cp_with_lo(c1, lmbda)), G),
        Transition(Side(b8), Side(c2, cp_with_lo(c3, lmbda)), G)
    ]
)

systems[7] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b2, cp_with_lo(a2, mu)), F),
        Transition(Side(a3), Side(b1, cp_with_lo(a4, mu)), F),

        Transition(Side(a2), Side(b4, cp_with_lo(b1, lmbda)), G),
        Transition(Side(a4), Side(b3, cp_with_lo(b2, lmbda)), G),

        Transition(Side(b1), Side(b6, cp_with_lo(b3, mu)), F),
        Transition(Side(b2), Side(b5, cp_with_lo(b4, mu)), F),

        Transition(Side(b3), Side(b8, cp_with_lo(b5, lmbda)), G),
        Transition(Side(b4), Side(b7, cp_with_lo(b6, lmbda)), G),

        Transition(Side(b5), Side(b10, cp_with_lo(b7, mu)), F),
        Transition(Side(b6), Side(b9, cp_with_lo(b8, mu)), F),

        Transition(Side(b7), Side(c3, cp_with_lo(b9, lmbda)), G),
        Transition(Side(b8), Side(c1, cp_with_lo(b10, lmbda)), G),

        Transition(Side(b9), Side(c4, cp_with_lo(c1, mu)), F),
        Transition(Side(b10), Side(c2, cp_with_lo(c3, mu)), F)
    ]
)
