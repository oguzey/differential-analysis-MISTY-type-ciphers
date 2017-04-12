from logger import logger
from system_transition import SystemTransition
from conditions import CustomConditions, Condition
from common_condition_generator import CommonConditionGenerator
from typing import List


def zero_conds_to_str(zero_conds: List[Condition]) -> str:
    return "Zero condition: %s" % "; ".join(map(str, zero_conds))


def non_zero_conds_to_str(non_zero_conds: List[Condition]) -> str:
    return "Non zero condition: %s" % "; ".join(map(str, non_zero_conds))


def main(system, inputs, outputs):
    ccond_generator = CommonConditionGenerator()
    logger.info("Basic system is: \n{}\n\n".format())
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

            logger.info("after apply conditions: \n", new_system)
            custom_cond = CustomConditions()
            new_system.simplify_with_custom_conditions(custom_cond)
            logger.info("after system analyze: \n", new_system)
            logger.info("all custom conditions: ",  custom_cond)
            if custom_cond.exist_contradiction(common_non_zero_conds):
                logger.info("New system has contradiction conditions.")
                logger.debug("FAIL SYSTEM!!!!")
                fails += 1
            elif new_system.do_fast_estimation(custom_cond, common_non_zero_conds):
                logger.info("CAN BE ESTIMATED  p^%d!!! All primitive transitions" % len(new_system))
                estimated += 1
                case_results.append(("p^%d" % len(new_system), pow(0.5, len(new_system))))
            else:
                logger.info("all custom conditions: ",  custom_cond)
                logger.info("after applying conditions: \n", new_system)
                logger.debug("=" * 50 + "end" + "=" * 50)
                SystemTransition.estimate(
                    new_system, custom_cond, in_cond, out_cond,
                    common_non_zero_conds, case_results, False)

            logger.debug("case res = " + str(case_results))
            results.append(case_results)
            logger.debug("=" * 150)

    logger.info("Total fails is %d" % fails)
    logger.info("Total estimated is %d" % estimated)

    uniq_estim = {}
    for x in range(len(results)):
        put_normalise_to_dict(results[x], uniq_estim, x)

    res = [(key, value) for key, value in list(uniq_estim.items())]
    return sorted(res, key=lambda pair: pair[0])

if __name__ == "__main__":
    with open('4_block_FC_res', 'w+', 0) as f:
        for key, value in list(four_blocks_systems.items()):
            res = main(value, [a1, a2, a3, a4], [g1, g2, g3, g4])
            f.write("%s rounds: \n" % str(key))
            for pair in res:
                est = "%s   [case %d]\n" % (pair[0], pair[1])
                logger.info(est)
                f.write(est)
            f.flush()
            f.write("Was analyze %d cases.\n\n" % SystemTransition.amount_cases)
            SystemTransition.amount_cases = 0  # reset for future cases
            f.flush()
