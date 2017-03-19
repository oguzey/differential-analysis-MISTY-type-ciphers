from variable import TypeVariable
from variable import Variable
from side import Side
from transition import Transition
from transition import SystemTransition
# from conditions import Condition
from conditions import CommonConditions
from conditions import CustomConditions
from test_for_res import put_normalise_to_dict

from FourCell import four_blocks_systems
from FourCell import a1
from FourCell import a2
from FourCell import a3
from FourCell import a4

from FourCell import g1
from FourCell import g2
from FourCell import g3
from FourCell import g4


def main(system, inputs, outputs):

    print "Basic system is: \n" + str(system) + "\n\n"

    print "Creating common conditions..."
    input_conditions = CommonConditions(*inputs)
    output_conditions = CommonConditions(*outputs)

    print "generating ..."
    print "input conditions... " + input_conditions.generate_conditions()
    print "output conditions... " + output_conditions.generate_conditions()

    amount_conditions = len(input_conditions)
    assert amount_conditions == len(output_conditions)
    print "Amount conditions is %d" % amount_conditions

    case = -1
    fails = 0
    estimated = 0
    results = []
    for input_index in xrange(amount_conditions):
        for output_index in xrange(amount_conditions):

            in_cond = input_conditions.get_condition(input_index)
            out_cond = output_conditions.get_condition(output_index)
            comcon_nz = list(in_cond.get_non_zero_condition())
            comcon_nz.extend(out_cond.get_non_zero_condition())

            print "=" * 50 + "start" + "=" * 50
            case_results = []
            case += 1
            print "case is %d" % case
            # if case < 59:
            #     continue
            # if case > 59:
            #     continue
            print "Input condition ", str(in_cond)
            print "Output condition ", str(out_cond)

            new_system = system.copy()
            # print "got next system: \n", new_system
            new_system.apply_common_condition(in_cond)
            new_system.apply_common_condition(out_cond)
            print "after apply conditions: \n", new_system
            custom_cond = CustomConditions()
            new_system.simplify_with_custom_conditions(custom_cond)
            print "after system analyse: \n", new_system
            print "all custom conditions: ",  custom_cond
            if custom_cond.exist_contradiction(comcon_nz):
                print "New system has contradiction conditions."
                print "FAIL SYSTEM!!!!"
                fails += 1
                # case_results.append(("Fail", -1))
            elif new_system.do_fast_estimation(custom_cond, comcon_nz):
                print "CAN BE ESTIMATED  p^%d!!! All primitive transitions" % len(new_system)
                estimated += 1
                case_results.append(("p^%d" % len(new_system), pow(0.5, len(new_system))))
            else:
                print "all custom conditions: ",  custom_cond
                print "after applying conditions: \n", new_system
                print "=" * 50 + "end" + "=" * 50
                SystemTransition.estimate(
                    new_system, custom_cond, in_cond, out_cond,
                    comcon_nz, case_results, False)

            print "case res = " + str(case_results)
            results.append(case_results)
            print "=" * 150

    print "Total fails is %d" % fails
    print "Total estimated is %d" % estimated

    print "+" * 120
    for x in xrange(len(results)):
        print "%d) %s" % (x, str(results[x]))
    print "+" * 120

    uniq_estim = {}
    for x in xrange(len(results)):

        # print "%d) before %s" % (x, str(results[x]))
        put_normalise_to_dict(results[x], uniq_estim, x)
        # print "%d) after %s" % (x, str(results[x]))

    #     while '' in results[x]:
    #         results[x].remove('')

    #     for value in results[x]:
    #         if value[1] > max_est[2]:
    #             max_est = (x + 1, value[0], value[1])
    #             print "NEW MAX " + str(max_est)

    # print "\nMax estimation is " + str(max_est)

    print "\n\n"
    res = [(key, value) for key, value in uniq_estim.items()]
    return sorted(res, key=lambda pair: pair[0])


f = open('4_block_FC_res', 'w+', 0)

for key, value in four_blocks_systems.items():
    res = main(value, [a1, a2, a3, a4], [g1, g2, g3, g4])
    f.write("%s rounds: \n" % str(key))
    for pair in res:
        est = "%s   [case %d]\n" % (pair[0], pair[1])
        print est
        f.write(est)
    f.flush()
    f.write("Was analyse %d cases.\n\n" % SystemTransition.amount_cases)
    SystemTransition.amount_cases = 0  # reset for future cases
    f.flush()

f.close()
