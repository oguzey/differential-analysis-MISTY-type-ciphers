from transition import Transition
from side import Side
from condition import ConditionState, Condition
from data.vars import *
from typing import Dict

cipher_name = 'skipjack'   # type: str
systems = dict()           # type: Dict[int, System]

# systems[3] = System(
#     inputs=[a1, a2, a3],
#     outputs=[c2, c3, c4],
#     transitions=[
#         Transition(Side(a1), Side(c2), F),
#         Transition(Side(a2, cp_with_lo(c2, lmbda)), Side(c3), G),
#         Transition(Side(a3, cp_with_lo(c3, mu)), Side(c4), F)
#     ]
# )  # c1 = a4 + lambda(c4)
########################################################################################################################
# For this system valid next equal b1 = c1 + mu(c4)

# Replace b1 with c5. Since we known about it all.
# cases:
# 1) c1 = 0, c4 = 0 => c5 = 0
# 2) c1 = 0, c4 != 0 => c5 != 0
# 3) c1 != 0, c4 = 0 => c5 != 0
# 4) c1 != 0, c4 != 0 => c5 = 0
# 5) c1 != 0, c4 != 0 => c5 != 0

def __condition_function_4(output_zero_conds):
    c1_is_zero = False
    c4_is_sero = False
    for zcond in output_zero_conds:
        if zcond.check_contains_var(c1, ConditionState.IS_ZERO):
            c1_is_zero = True
        elif zcond.check_contains_var(c4, ConditionState.IS_ZERO):
            c4_is_sero = True

    if c1_is_zero and c4_is_sero:
        return [Condition.create_zero_condition(Side(c5))]
    elif (c1_is_zero and not c4_is_sero) or (not c1_is_zero and c4_is_sero):
        return [Condition.create_non_zero_condition(Side(c5))]
    else:  #  (not c1_is_zero and not c4_is_sero)
        return [Condition.create_zero_condition(Side(c5)), Condition.create_non_zero_condition(Side(c5))]

systems[4] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(c5), F),                                                       #  Transition(Side(a1), Side(b1), F),
        Transition(Side(a2, cp_with_lo(c5, lmbda)), Side(c2), G),                      #  Transition(Side(a2, cp_with_lo(b1, lmbda)), Side(c2), G),
        Transition(Side(a3, cp_with_lo(c2, mu)), Side(c3), F),
        Transition(Side(a4, cp_with_lo(c3, lmbda)), Side(c4), G)
    ],
    condition_func=__condition_function_4
)  # b1 = c1 + mu(c4)



########################################################################################################################
# systems[5] = System(
#     inputs=[a1, a2, a3, a4],
#     outputs=[c2, c3, c4],
#     transitions=[
#         Transition(Side(a1), Side(b1), F),
#         Transition(Side(a2, cp_with_lo(b1, lmbda)), Side(c1, cp_with_lo(c4, lmbda)), G),                          # Transition(Side(a2, cp_with_lo(b1, lmbda)), Side(b2), G)
#         Transition(Side(a3, cp_with_lo(c1, mu), cp_with_lo(c4, lmbda, mu)), Side(c2), F),                         # Transition(Side(a3, cp_with_lo(b2, mu)), Side(c2), F),
#         Transition(Side(a4, cp_with_lo(c2, lmbda)), Side(c3), G),
#         Transition(Side(b1, cp_with_lo(c3, mu)), Side(c4), F)
#     ]
# )  # b2 = c1 + lambda(c4)
