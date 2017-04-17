from logger import logger
from system_transition import SystemTransition
from conditions import CustomConditions, Condition
from common_condition_generator import CommonConditionGenerator
from variable import Variable, TypeVariable
from transition import Transition, BlockFunction
from side import Side
from typing import List


def zero_conds_to_str(zero_conds: List[Condition]) -> str:
    return "Zero condition: %s" % "; ".join(map(str, zero_conds))


def non_zero_conds_to_str(non_zero_conds: List[Condition]) -> str:
    return "Non zero condition: %s" % "; ".join(map(str, non_zero_conds))


def main(system, inputs, outputs):
    ccond_generator = CommonConditionGenerator()
    logger.info("Basic system is: \n{}\n\n".format(system))
    logger.info("Creating common conditions...")

    input_conditions = ccond_generator.gen_all_common_conditions(inputs)
    output_conditions = ccond_generator.gen_all_common_conditions(outputs)

    amount_conditions = len(input_conditions)
    assert amount_conditions == len(output_conditions)
    logger.info("Amount conditions is %d" % amount_conditions)

    case = -1
    fails = 0
    estimated = 0
    results = []
    for in_zero_conds, in_non_zero_conds in input_conditions:
        for out_zero_conds, out_non_zero_conds in output_conditions:
            # Debug informations
            case += 1
            logger.debug("case is {} ".format(case))
            logger.debug("=" * 50 + "start" + "=" * 50)
            # end

            logger.info("Input condition: \n\t{}\n\t{}".format(zero_conds_to_str(in_zero_conds),
                                                               non_zero_conds_to_str(in_non_zero_conds)))
            logger.info("Output condition: \n\t{}\n\t{}".format(zero_conds_to_str(out_zero_conds),
                                                                non_zero_conds_to_str(out_non_zero_conds)))

            common_non_zero_conds = list(in_non_zero_conds)
            common_non_zero_conds.extend(out_non_zero_conds)

            case_results = []
            new_system = system.copy()
            # Apply all zero conditions and drop them as variables became zero
            for x in in_zero_conds:
                new_system.apply_condition(x)
            for x in out_zero_conds:
                new_system.apply_condition(x)

            logger.info("after apply conditions: \n{}".format(new_system))
            custom_cond = CustomConditions()
            new_system.simplify_with_custom_conditions(custom_cond)
            logger.info("after system analyze: \n{}".format(new_system))
            logger.info("all custom conditions: {}".format(custom_cond))
            if custom_cond.exist_contradiction(common_non_zero_conds):
                logger.info("New system has contradiction conditions.")
                logger.debug("FAIL SYSTEM!!!!")
                fails += 1
            elif new_system.do_fast_estimation(custom_cond, common_non_zero_conds):
                logger.info("CAN BE ESTIMATED  p^%d!!! All primitive transitions" % len(new_system))
                estimated += 1
                case_results.append(("p^%d" % len(new_system), pow(0.5, len(new_system))))
            else:
                logger.info("all custom conditions: {}".format(custom_cond))
                logger.info("after applying conditions: \n{}".format(new_system))
                logger.debug("=" * 50 + "end" + "=" * 50)
                SystemTransition.estimate(
                    new_system, custom_cond, (in_zero_conds, in_non_zero_conds), (out_zero_conds, out_non_zero_conds),
                    common_non_zero_conds, case_results, False)

            logger.debug("case res = " + str(case_results))
            results.append(case_results)
            logger.debug("=" * 150)

    logger.info("Total fails is %d" % fails)
    logger.info("Total estimated is %d" % estimated)

    return results

if __name__ == "__main__":

    a1 = Variable(TypeVariable.INPUT)
    a2 = Variable(TypeVariable.INPUT)

    b1 = Variable(TypeVariable.UNKNOWN)

    c1 = Variable(TypeVariable.OUTPUT)
    c2 = Variable(TypeVariable.OUTPUT)

    system = SystemTransition(Transition(Side(a1), Side(b1, a2), BlockFunction('F', 'p')),
                              Transition(Side(a2), Side(c2, b1), BlockFunction('G', 'q')),
                              Transition(Side(b1), Side(c1, c2), BlockFunction('F', 'p')))

    res = main(system, [a1, a2], [c1, c2])
    logger.info("System with %d rounds: " % system.amount_rounds())
    for pair in res:
        for est in pair:
            logger.info("{}".format(est))

    logger.info("Was analyze %d cases.\n\n" % SystemTransition.amount_cases)
    SystemTransition.amount_cases = 0  # reset for future cases
