from transition import Transition
from side import Side
from data.vars import *
from typing import Dict

cipher_name = 'misty'   # type: str
systems = dict()        # type: Dict[int, System]


systems[3] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(c2, cp_with_lo(a2, mu)), F),
        Transition(Side(a2), Side(c3, cp_with_lo(a3, lmbda)), G),
        Transition(Side(a3), Side(c4, cp_with_lo(a4, mu)), F),
    ]
)

systems[4] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(c1, cp_with_lo(a2, mu)), F),
        Transition(Side(a2), Side(c2, cp_with_lo(a3, lmbda)), G),
        Transition(Side(a3), Side(c3, cp_with_lo(a4, mu)), F),
        Transition(Side(a4), Side(c4, cp_with_lo(c1, lmbda)), G)
    ]
)

systems[5] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1, cp_with_lo(a2, mu)), F),
        Transition(Side(a2), Side(c1, cp_with_lo(a3, lmbda)), G),
        Transition(Side(a3), Side(c2, cp_with_lo(a4, mu)), F),
        Transition(Side(a4), Side(c3, cp_with_lo(b1, lmbda)), G),
        Transition(Side(b1), Side(c4, cp_with_lo(c1, mu)), F)
    ]
)


systems[6] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1, cp_with_lo(a2, mu)), F),
        Transition(Side(a2), Side(b2, cp_with_lo(a3, lmbda)), G),
        Transition(Side(a3), Side(c1, cp_with_lo(a4, mu)), F),
        Transition(Side(a4), Side(c2, cp_with_lo(b1, lmbda)), G),
        Transition(Side(b1), Side(c3, cp_with_lo(b2, mu)), F),
        Transition(Side(b2), Side(c4, cp_with_lo(c1, lmbda)), G)
    ]
)

systems[7] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1, cp_with_lo(a2, mu)), F),
        Transition(Side(a2), Side(b2, cp_with_lo(a3, lmbda)), G),
        Transition(Side(a3), Side(b3, cp_with_lo(a4, mu)), F),
        Transition(Side(a4), Side(c1, cp_with_lo(b1, lmbda)), G),
        Transition(Side(b1), Side(c2, cp_with_lo(b2, mu)), F),
        Transition(Side(b2), Side(c3, cp_with_lo(b3, lmbda)), G),
        Transition(Side(b3), Side(c4, cp_with_lo(c1, mu)), F)
    ]
)

systems[8] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1, cp_with_lo(a2, mu)), F),
        Transition(Side(a2), Side(b2, cp_with_lo(a3, lmbda)), G),
        Transition(Side(a3), Side(b3, cp_with_lo(a4, mu)), F),
        Transition(Side(a4), Side(b4, cp_with_lo(b1, lmbda)), G),
        Transition(Side(b1), Side(c1, cp_with_lo(b2, mu)), F),
        Transition(Side(b2), Side(c2, cp_with_lo(b3, lmbda)), G),
        Transition(Side(b3), Side(c3, cp_with_lo(b4, mu)), F),
        Transition(Side(b4), Side(c4, cp_with_lo(c1, lmbda)), G)
    ]
)

systems[9] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1, cp_with_lo(a2, mu)), F),
        Transition(Side(a2), Side(b2, cp_with_lo(a3, lmbda)), G),
        Transition(Side(a3), Side(b3, cp_with_lo(a4, mu)), F),
        Transition(Side(a4), Side(b4, cp_with_lo(b1, lmbda)), G),
        Transition(Side(b1), Side(b5, cp_with_lo(b2, mu)), F),
        Transition(Side(b2), Side(c1, cp_with_lo(b3, lmbda)), G),
        Transition(Side(b3), Side(c2, cp_with_lo(b4, mu)), F),
        Transition(Side(b4), Side(c3, cp_with_lo(b5, lmbda)), G),
        Transition(Side(b5), Side(c4, cp_with_lo(c1, mu)), F)
    ]
)

systems[10] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1, cp_with_lo(a2, mu)), F),
        Transition(Side(a2), Side(b2, cp_with_lo(a3, lmbda)), G),
        Transition(Side(a3), Side(b3, cp_with_lo(a4, mu)), F),
        Transition(Side(a4), Side(b4, cp_with_lo(b1, lmbda)), G),
        Transition(Side(b1), Side(b5, cp_with_lo(b2, mu)), F),
        Transition(Side(b2), Side(b6, cp_with_lo(b3, lmbda)), G),
        Transition(Side(b3), Side(c1, cp_with_lo(b4, mu)), F),
        Transition(Side(b4), Side(c2, cp_with_lo(b5, lmbda)), G),
        Transition(Side(b5), Side(c3, cp_with_lo(b6, mu)), F),
        Transition(Side(b6), Side(c4, cp_with_lo(c1, lmbda)), G)
    ]
)

systems[11] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1, cp_with_lo(a2, mu)), F),
        Transition(Side(a2), Side(b2, cp_with_lo(a3, lmbda)), G),
        Transition(Side(a3), Side(b3, cp_with_lo(a4, mu)), F),
        Transition(Side(a4), Side(b4, cp_with_lo(b1, lmbda)), G),
        Transition(Side(b1), Side(b5, cp_with_lo(b2, mu)), F),
        Transition(Side(b2), Side(b6, cp_with_lo(b3, lmbda)), G),
        Transition(Side(b3), Side(b7, cp_with_lo(b4, mu)), F),
        Transition(Side(b4), Side(c1, cp_with_lo(b5, lmbda)), G),
        Transition(Side(b5), Side(c2, cp_with_lo(b6, mu)), F),
        Transition(Side(b6), Side(c3, cp_with_lo(b7, lmbda)), G),
        Transition(Side(b7), Side(c4, cp_with_lo(c1, mu)), F)
    ]
)

systems[12] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1, cp_with_lo(a2, mu)), F),
        Transition(Side(a2), Side(b2, cp_with_lo(a3, lmbda)), G),
        Transition(Side(a3), Side(b3, cp_with_lo(a4, mu)), F),
        Transition(Side(a4), Side(b4, cp_with_lo(b1, lmbda)), G),
        Transition(Side(b1), Side(b5, cp_with_lo(b2, mu)), F),
        Transition(Side(b2), Side(b6, cp_with_lo(b3, lmbda)), G),
        Transition(Side(b3), Side(b7, cp_with_lo(b4, mu)), F),
        Transition(Side(b4), Side(b8, cp_with_lo(b5, lmbda)), G),
        Transition(Side(b5), Side(c1, cp_with_lo(b6, mu)), F),
        Transition(Side(b6), Side(c2, cp_with_lo(b7, lmbda)), G),
        Transition(Side(b7), Side(c3, cp_with_lo(b8, mu)), F),
        Transition(Side(b8), Side(c4, cp_with_lo(c1, lmbda)), G)
    ]
)

systems[13] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1, cp_with_lo(a2, mu)), F),
        Transition(Side(a2), Side(b2, cp_with_lo(a3, lmbda)), G),
        Transition(Side(a3), Side(b3, cp_with_lo(a4, mu)), F),
        Transition(Side(a4), Side(b4, cp_with_lo(b1, lmbda)), G),
        Transition(Side(b1), Side(b5, cp_with_lo(b2, mu)), F),
        Transition(Side(b2), Side(b6, cp_with_lo(b3, lmbda)), G),
        Transition(Side(b3), Side(b7, cp_with_lo(b4, mu)), F),
        Transition(Side(b4), Side(b8, cp_with_lo(b5, lmbda)), G),
        Transition(Side(b5), Side(b9, cp_with_lo(b6, mu)), F),
        Transition(Side(b6), Side(c1, cp_with_lo(b7, lmbda)), G),
        Transition(Side(b7), Side(c2, cp_with_lo(b8, mu)), F),
        Transition(Side(b8), Side(c3, cp_with_lo(b9, lmbda)), G),
        Transition(Side(b9), Side(c4, cp_with_lo(c1, mu)), F)
    ]
)

systems[14] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1, cp_with_lo(a2, mu)), F),
        Transition(Side(a2), Side(b2, cp_with_lo(a3, lmbda)), G),
        Transition(Side(a3), Side(b3, cp_with_lo(a4, mu)), F),
        Transition(Side(a4), Side(b4, cp_with_lo(b1, lmbda)), G),
        Transition(Side(b1), Side(b5, cp_with_lo(b2, mu)), F),
        Transition(Side(b2), Side(b6, cp_with_lo(b3, lmbda)), G),
        Transition(Side(b3), Side(b7, cp_with_lo(b4, mu)), F),
        Transition(Side(b4), Side(b8, cp_with_lo(b5, lmbda)), G),
        Transition(Side(b5), Side(b9, cp_with_lo(b6, mu)), F),
        Transition(Side(b6), Side(b10, cp_with_lo(b7, lmbda)), G),
        Transition(Side(b7), Side(c1, cp_with_lo(b8, mu)), F),
        Transition(Side(b8), Side(c2, cp_with_lo(b9, lmbda)), G),
        Transition(Side(b9), Side(c3, cp_with_lo(b10, mu)), F),
        Transition(Side(b10), Side(c4, cp_with_lo(c1, lmbda)), G)
    ]
)
