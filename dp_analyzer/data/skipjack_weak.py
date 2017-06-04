from transition import Transition
from side import Side
from condition import ConditionState, Condition
from data.vars import *
from typing import Dict, List

cipher_name = 'skipjack_weak'   # type: str
systems = dict()           # type: Dict[int, System]


def __generate_condition_func(zero_conds: List[Condition], var: Variable, var_with_lo: Variable, var_output: Variable):
    var_is_zero = False
    var_with_lo_is_zero = False
    for zcond in zero_conds:
        if zcond.check_contains_var(var, ConditionState.IS_ZERO):
            var_is_zero = True
        elif zcond.check_contains_var(var_with_lo, ConditionState.IS_ZERO):
            var_with_lo_is_zero = True

    if var_is_zero and var_with_lo_is_zero:
        return [Condition.create_zero_condition(Side(var_output.clone()))]
    elif (var_is_zero and not var_with_lo_is_zero) or (not var_is_zero and var_with_lo_is_zero):
        return [Condition.create_non_zero_condition(Side(var_output.clone()))]
    else:  # (not var_is_zero and not var_with_lo_is_zero)
        return [Condition.create_zero_condition(Side(var_output.clone())),
                Condition.create_non_zero_condition(Side(var_output.clone()))]

########################################################################################################################
# For this system valid next equal c1 = a4 + lambda(c4)

systems[3] = System(
    inputs=[a1, a2, a3],
    outputs=[c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(c2), G),
        Transition(Side(a2, cp_with_lo(c2, mu)),    Side(c3), F),
        Transition(Side(a3, cp_with_lo(c3, lmbda)), Side(c4), G)
    ]
)

########################################################################################################################
# Cases for c5:
# 1) c1 = 0, c4 = 0 => c5 = 0
# 2) c1 = 0, c4 != 0 => c5 != 0
# 3) c1 != 0, c4 = 0 => c5 != 0
# 4) c1 != 0, c4 != 0 => c5 = 0
# 5) c1 != 0, c4 != 0 => c5 != 0
########################################################################################################################

systems[4] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(c5), G),
        Transition(Side(a2, cp_with_lo(c5, mu)),    Side(c2), F),
        Transition(Side(a3, cp_with_lo(c2, lmbda)), Side(c3), G),
        Transition(Side(a4, cp_with_lo(c3, mu)),    Side(c4), F)
    ],
    condition_func=lambda output_zero_conds: __generate_condition_func(output_zero_conds, c1, c4, c5)
)   # b1 = c1 + mu(c4)  =>  c5 =c1 + mu(c4)

systems[5] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1), G),
        Transition(Side(a2, cp_with_lo(b1, mu)),    Side(c5), F),
        Transition(Side(a3, cp_with_lo(c5, lmbda)), Side(c2), G),
        Transition(Side(a4, cp_with_lo(c2, mu)),    Side(c3), F),
        Transition(Side(b1, cp_with_lo(c3, lmbda)), Side(c4), G)
    ],
    condition_func=lambda output_zero_conds: __generate_condition_func(output_zero_conds, c1, c4, c5)
)   # b2 = c1 + lambda(c4)  =>  c5 = c1 + lambda(c4)

systems[6] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1), G),
        Transition(Side(a2, cp_with_lo(b1, mu)),    Side(b2), F),
        Transition(Side(a3, cp_with_lo(b2, lmbda)), Side(c5), G),
        Transition(Side(a4, cp_with_lo(c5, mu)),    Side(c2), F),
        Transition(Side(b1, cp_with_lo(c2, lmbda)), Side(c3), G),
        Transition(Side(b2, cp_with_lo(c3, mu)),    Side(c4), F)
    ],
    condition_func=lambda output_zero_conds: __generate_condition_func(output_zero_conds, c1, c4, c5)
)   # b3 = c1 + mu(c4)  =>  c5 = c1 + mu(c4)

systems[7] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1), G),
        Transition(Side(a2, cp_with_lo(b1, mu)),    Side(b2), F),
        Transition(Side(a3, cp_with_lo(b2, lmbda)), Side(b3), G),
        Transition(Side(a4, cp_with_lo(b3, mu)),    Side(c5), F),
        Transition(Side(b1, cp_with_lo(c5, lmbda)), Side(c2), G),
        Transition(Side(b2, cp_with_lo(c2, mu)),    Side(c3), F),
        Transition(Side(b3, cp_with_lo(c3, lmbda)), Side(c4), G)
    ],
    condition_func=lambda output_zero_conds: __generate_condition_func(output_zero_conds, c1, c4, c5)
)   # b4 = c1 + lambda(c4)  =>  c5 = c1 + lambda(c4)

systems[8] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1), G),
        Transition(Side(a2, cp_with_lo(b1, mu)),    Side(b2), F),
        Transition(Side(a3, cp_with_lo(b2, lmbda)), Side(b3), G),
        Transition(Side(a4, cp_with_lo(b3, mu)),    Side(b4), F),
        Transition(Side(b1, cp_with_lo(b4, lmbda)), Side(c5), G),
        Transition(Side(b2, cp_with_lo(c5, mu)),    Side(c2), F),
        Transition(Side(b3, cp_with_lo(c2, lmbda)), Side(c3), G),
        Transition(Side(b4, cp_with_lo(c3, mu)),    Side(c4), F)
    ],
    condition_func=lambda output_zero_conds: __generate_condition_func(output_zero_conds, c1, c4, c5)
)   # b5 = c1 + mu(c4)  =>  c5 = c1 + mu(c4)

systems[9] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1), G),
        Transition(Side(a2, cp_with_lo(b1, mu)),    Side(b2), F),
        Transition(Side(a3, cp_with_lo(b2, lmbda)), Side(b3), G),
        Transition(Side(a4, cp_with_lo(b3, mu)),    Side(b4), F),
        Transition(Side(b1, cp_with_lo(b4, lmbda)), Side(b5), G),
        Transition(Side(b2, cp_with_lo(b5, mu)),    Side(c5), F),
        Transition(Side(b3, cp_with_lo(c5, lmbda)), Side(c2), G),
        Transition(Side(b4, cp_with_lo(c2, mu)),    Side(c3), F),
        Transition(Side(b5, cp_with_lo(c3, lmbda)), Side(c4), G)
    ],
    condition_func=lambda output_zero_conds: __generate_condition_func(output_zero_conds, c1, c4, c5)
)   # b6 = c1 + lambda(c4)  =>  c5 = c1 + lambda(c4)

systems[10] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1), G),
        Transition(Side(a2, cp_with_lo(b1, mu)),    Side(b2), F),
        Transition(Side(a3, cp_with_lo(b2, lmbda)), Side(b3), G),
        Transition(Side(a4, cp_with_lo(b3, mu)),    Side(b4), F),
        Transition(Side(b1, cp_with_lo(b4, lmbda)), Side(b5), G),
        Transition(Side(b2, cp_with_lo(b5, mu)),    Side(b6), F),
        Transition(Side(b3, cp_with_lo(b6, lmbda)), Side(c5), G),
        Transition(Side(b4, cp_with_lo(c5, mu)),    Side(c2), F),
        Transition(Side(b5, cp_with_lo(c2, lmbda)), Side(c3), G),
        Transition(Side(b6, cp_with_lo(c3, mu)),    Side(c4), F)
    ],
    condition_func=lambda output_zero_conds: __generate_condition_func(output_zero_conds, c1, c4, c5)
)   # b7 = c1 + mu(c4)  =>  c5 = c1 + mu(c4)

systems[11] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1), G),
        Transition(Side(a2, cp_with_lo(b1, mu)),    Side(b2), F),
        Transition(Side(a3, cp_with_lo(b2, lmbda)), Side(b3), G),
        Transition(Side(a4, cp_with_lo(b3, mu)),    Side(b4), F),
        Transition(Side(b1, cp_with_lo(b4, lmbda)), Side(b5), G),
        Transition(Side(b2, cp_with_lo(b5, mu)),    Side(b6), F),
        Transition(Side(b3, cp_with_lo(b6, lmbda)), Side(b7), G),
        Transition(Side(b4, cp_with_lo(b7, mu)),    Side(c5), F),
        Transition(Side(b5, cp_with_lo(c5, lmbda)), Side(c2), G),
        Transition(Side(b6, cp_with_lo(c2, mu)),    Side(c3), F),
        Transition(Side(b7, cp_with_lo(c3, lmbda)), Side(c4), G)
    ],
    condition_func=lambda output_zero_conds: __generate_condition_func(output_zero_conds, c1, c4, c5)
)   # b8 = c1 + lambda(c4)  =>  c5 = c1 + lambda(c4)

systems[12] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1), G),
        Transition(Side(a2, cp_with_lo(b1, mu)),    Side(b2), F),
        Transition(Side(a3, cp_with_lo(b2, lmbda)), Side(b3), G),
        Transition(Side(a4, cp_with_lo(b3, mu)),    Side(b4), F),
        Transition(Side(b1, cp_with_lo(b4, lmbda)), Side(b5), G),
        Transition(Side(b2, cp_with_lo(b5, mu)),    Side(b6), F),
        Transition(Side(b3, cp_with_lo(b6, lmbda)), Side(b7), G),
        Transition(Side(b4, cp_with_lo(b7, mu)),    Side(b8), F),
        Transition(Side(b5, cp_with_lo(b8, lmbda)), Side(c5), G),
        Transition(Side(b6, cp_with_lo(c5, mu)),    Side(c2), F),
        Transition(Side(b7, cp_with_lo(c2, lmbda)), Side(c3), G),
        Transition(Side(b8, cp_with_lo(c3, mu)),    Side(c4), F)
    ],
    condition_func=lambda output_zero_conds: __generate_condition_func(output_zero_conds, c1, c4, c5)
)   # b9 = c1 + mu(c4)  =>  c5 = c1 + mu(c4)

systems[13] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1), G),
        Transition(Side(a2, cp_with_lo(b1, mu)),    Side(b2), F),
        Transition(Side(a3, cp_with_lo(b2, lmbda)), Side(b3), G),
        Transition(Side(a4, cp_with_lo(b3, mu)),    Side(b4), F),
        Transition(Side(b1, cp_with_lo(b4, lmbda)), Side(b5), G),
        Transition(Side(b2, cp_with_lo(b5, mu)),    Side(b6), F),
        Transition(Side(b3, cp_with_lo(b6, lmbda)), Side(b7), G),
        Transition(Side(b4, cp_with_lo(b7, mu)),    Side(b8), F),
        Transition(Side(b5, cp_with_lo(b8, lmbda)), Side(b9), G),
        Transition(Side(b6, cp_with_lo(b9, mu)),    Side(c5), F),
        Transition(Side(b7, cp_with_lo(c5, lmbda)), Side(c2), G),
        Transition(Side(b8, cp_with_lo(c2, mu)),    Side(c3), F),
        Transition(Side(b9, cp_with_lo(c3, lmbda)), Side(c4), G)
    ],
    condition_func=lambda output_zero_conds: __generate_condition_func(output_zero_conds, c1, c4, c5)
)   # b10 = c1 + lambda(c4)  =>  c5 = c1 + lambda(c4)

systems[14] = System(
    inputs=[a1, a2, a3, a4],
    outputs=[c1, c2, c3, c4],
    transitions=[
        Transition(Side(a1), Side(b1), G),
        Transition(Side(a2, cp_with_lo(b1, mu)),    Side(b2), F),
        Transition(Side(a3, cp_with_lo(b2, lmbda)), Side(b3), G),
        Transition(Side(a4, cp_with_lo(b3, mu)),    Side(b4), F),
        Transition(Side(b1, cp_with_lo(b4, lmbda)), Side(b5), G),
        Transition(Side(b2, cp_with_lo(b5, mu)),    Side(b6), F),
        Transition(Side(b3, cp_with_lo(b6, lmbda)), Side(b7), G),
        Transition(Side(b4, cp_with_lo(b7, mu)),    Side(b8), F),
        Transition(Side(b5, cp_with_lo(b8, lmbda)), Side(b9), G),
        Transition(Side(b6, cp_with_lo(b9, mu)),    Side(b10), F),
        Transition(Side(b7, cp_with_lo(b10, lmbda)),Side(c5), G),
        Transition(Side(b8, cp_with_lo(c5, mu)),    Side(c2), F),
        Transition(Side(b9, cp_with_lo(c2, lmbda)), Side(c3), G),
        Transition(Side(b10, cp_with_lo(c3, mu)),   Side(c4), F)
    ],
    condition_func=lambda output_zero_conds: __generate_condition_func(output_zero_conds, c1, c4, c5)
)   # b11 = c1 + mu(c4)  =>  c5 = c1 + mu(c4)
