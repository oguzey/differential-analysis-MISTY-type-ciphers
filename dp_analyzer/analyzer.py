from logger import logger
from transition import SystemTransition
from conditions import CommonConditions, CustomConditions
from test_for_res import put_normalise_to_dict

from FourCell import four_blocks_systems
from FourCell import a1, a2, a3, a4
from FourCell import g1, g2, g3, g4


def main(system, inputs, outputs):
    logger.info("Basic system is: \n{}\n\n".format())
    logger.info("Creating common conditions...")

    input_conditions = CommonConditions(*inputs)
    output_conditions = CommonConditions(*outputs)

    amount_conditions = len(input_conditions)
    assert amount_conditions == len(output_conditions)
    logger.info("Amount conditions is %d" % amount_conditions)

    case = -1
    fails = 0
    estimated = 0
    results = []
    for input_index in range(amount_conditions):
        for output_index in range(amount_conditions):

            in_cond = input_conditions.get_condition(input_index)
            out_cond = output_conditions.get_condition(output_index)
            comcon_nz = list(in_cond.get_non_zero_condition())
            comcon_nz.extend(out_cond.get_non_zero_condition())

            logger.debug("=" * 50 + "start" + "=" * 50)
            case_results = []
            case += 1
            logger.debug("case is %d" % case)
            logger.info("Input condition ", str(in_cond))
            logger.info("Output condition ", str(out_cond))

            new_system = system.copy()
            new_system.apply_common_condition(in_cond)
            new_system.apply_common_condition(out_cond)
            logger.info("after apply conditions: \n", new_system)
            custom_cond = CustomConditions()
            new_system.simplify_with_custom_conditions(custom_cond)
            logger.info("after system analyze: \n", new_system)
            logger.info("all custom conditions: ",  custom_cond)
            if custom_cond.exist_contradiction(comcon_nz):
                logger.info("New system has contradiction conditions.")
                logger.debug("FAIL SYSTEM!!!!")
                fails += 1
            elif new_system.do_fast_estimation(custom_cond, comcon_nz):
                logger.info("CAN BE ESTIMATED  p^%d!!! All primitive transitions" % len(new_system))
                estimated += 1
                case_results.append(("p^%d" % len(new_system), pow(0.5, len(new_system))))
            else:
                logger.info("all custom conditions: ",  custom_cond)
                logger.info("after applying conditions: \n", new_system)
                logger.debug("=" * 50 + "end" + "=" * 50)
                SystemTransition.estimate(
                    new_system, custom_cond, in_cond, out_cond,
                    comcon_nz, case_results, False)

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
