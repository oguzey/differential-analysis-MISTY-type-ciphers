from transition import Transition
from side import Side
from data.vars import *
from typing import Dict

cipher_name = 'misty'   # type: str
systems = dict()        # type: Dict[int, System]


# systems[6] = System(
#     inputs=[a1, a2, a3, a4],
#     outputs=[c1, c2, c3, c4],
#     transitions=[
#         Transition(Side(a1), Side(b1, cp_and_use_lo(a2, mu)), F),
#         Transition(Side(a2), Side(b2, cp_and_use_lo(a3, lmbda)), G),
#         Transition(Side(a3), Side(c1, cp_and_use_lo(a4, mu)), F),
#         Transition(Side(a4), Side(c2, cp_and_use_lo(b1, lmbda)), G),
#         Transition(Side(b1), Side(c3, cp_and_use_lo(b2, mu)), F),
#         Transition(Side(b2), Side(c4, cp_and_use_lo(c1, lmbda)), G)
#     ]
# )

systems[7] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1, cp_and_use_lo(a2, mu)), F),
        Transition(Side(a2), Side(b2, cp_and_use_lo(a3, lmbda)), G),
        Transition(Side(a3), Side(b3, cp_and_use_lo(a4, mu)), F),
        Transition(Side(a4), Side(c1, cp_and_use_lo(b1, lmbda)), G),
        Transition(Side(b1), Side(c2, cp_and_use_lo(b2, mu)), F),
        Transition(Side(b2), Side(c3, cp_and_use_lo(b3, lmbda)), G),
        Transition(Side(b3), Side(c4, cp_and_use_lo(c1, mu)), F)
    ]
)
