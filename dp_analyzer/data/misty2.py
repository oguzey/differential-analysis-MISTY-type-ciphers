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

# systems[3] = System(
#     inputs=[a1, a2, a3, a4],
#     outputs=[c1, c2, c3, c4],
#     transitions=[
#         # Transition(Side(a1), Side(b2, cp_with_lo(a2, mu)), F),
#         # Transition(Side(a3), Side(b1, cp_with_lo(a4, mu)), F),
#         #
#         # Transition(Side(a2), Side(b4, cp_with_lo(b1, lmbda)), G),
#         # Transition(Side(a4), Side(b3, cp_with_lo(b2, lmbda)), G),
#         #
#         # Transition(Side(b1), Side(c3, cp_with_lo(b3, mu)), F),
#         # Transition(Side(b2), Side(c1, cp_with_lo(b4, mu)), F)
#     ]
# )

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