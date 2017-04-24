from logger import logger
from system_transition import SystemTransition
from conditions import CustomConditions, Condition
from common_condition_generator import CommonConditionGenerator
from variable import Variable, TypeVariable
from transition import Transition, BlockFunction
from side import Side
from typing import List
import multiprocessing as mp
import time


def zero_conds_to_str(zero_conds: List[Condition]) -> str:
    return "Zero condition: %s" % "; ".join(map(str, zero_conds))


def non_zero_conds_to_str(non_zero_conds: List[Condition]) -> str:
    return "Non zero condition: %s" % "; ".join(map(str, non_zero_conds))


def worker(system, input_tasks, done_tasks):
    logger.info('[{}.{}] got system \n{}'.format(mp.current_process().name, mp.current_process().pid, system))
    # TODO: pass input_tasks to estimate method to reduce timeout waiting new tasks
    system.get_estimate()
    # after get_estimate we should get estimate so we can add the system to done_tasks
    done_tasks.put(system)
    input_tasks.put('no-task')


def main(system, inputs, outputs):
    logger.info("Basic system is: \n{}\n\n".format(system))

    logger.info("Creating common conditions...")
    ccond_generator = CommonConditionGenerator()
    input_conditions = ccond_generator.gen_all_common_conditions(inputs)
    output_conditions = ccond_generator.gen_all_common_conditions(outputs)

    assert len(input_conditions) == len(output_conditions)
    logger.info("Amount conditions is %d" % len(input_conditions))

    logger.info("Generating systems...")
    mp_manager = mp.Manager()
    input_tasks = mp_manager.Queue()
    done_tasks = mp_manager.Queue()
    logger.info("Created input_tasks = {}, done_tasks = {}".format(input_tasks, done_tasks))
    for in_zero_conds, in_non_zero_conds in input_conditions:
        for out_zero_conds, out_non_zero_conds in output_conditions:
            logger.info("Input condition: \n\t{}\n\t{}".format(zero_conds_to_str(in_zero_conds),
                                                               non_zero_conds_to_str(in_non_zero_conds)))
            logger.info("Output condition: \n\t{}\n\t{}".format(zero_conds_to_str(out_zero_conds),
                                                                non_zero_conds_to_str(out_non_zero_conds)))
            new_system = system.copy()
            new_system.set_common_conditions(in_zero_conds, in_non_zero_conds, out_zero_conds, out_non_zero_conds)
            input_tasks.put(new_system)

    logger.info("Estimating...")
    with mp.Pool(processes=mp.cpu_count()) as pool:
        logger.debug('Pool with {} process created'.format(mp.cpu_count()))

        counter = 1
        system = input_tasks.get_nowait()
        pool.apply_async(worker, (system, input_tasks, done_tasks))

        while counter > 0:
            system = input_tasks.get(block=True)
            if system == 'no-task':
                counter -= 1
            else:
                counter += 1
                pool.apply_async(worker, (system, input_tasks, done_tasks))

    logger.info("Done total tasks - {}".format(done_tasks.qsize()))
    logger.info("Results:")
    while done_tasks.qsize() > 0:
        system = done_tasks.get_nowait()
        logger.info("\testimate: {}".format(system.get_mark()))
    # logger.info("Total fails is %d" % fails)
    # logger.info("Total estimated is %d" % estimated)


if __name__ == "__main__":

    a1 = Variable(TypeVariable.INPUT)
    a2 = Variable(TypeVariable.INPUT)

    b1 = Variable(TypeVariable.UNKNOWN)

    c1 = Variable(TypeVariable.OUTPUT)
    c2 = Variable(TypeVariable.OUTPUT)

    st = SystemTransition(Transition(Side(a1), Side(b1, a2), BlockFunction('F', 'p')),
                              Transition(Side(a2), Side(c2, b1), BlockFunction('G', 'q')),
                              Transition(Side(b1), Side(c1, c2), BlockFunction('F', 'p')))

    main(st, [a1, a2], [c1, c2])
    # logger.info("System with %d rounds: " % system.amount_rounds())
    # for pair in res:
    #     for est in pair:
    #         logger.info("{}".format(est))
    #
    # logger.info("Was analyze %d cases.\n\n" % SystemTransition.amount_cases)
    # SystemTransition.amount_cases = 0  # reset for future cases
