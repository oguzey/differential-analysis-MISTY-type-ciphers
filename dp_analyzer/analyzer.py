#!/usr/bin/python3

from logger import logger
from system_transition import SystemTransition
from condition import Condition
from common_condition_generator import CommonConditionGenerator
from variable import Variable, TypeVariable
from transition import Transition, BlockFunction
from linear_operator import LOMu, LOLambda
from side import Side
from typing import List
import multiprocessing as mp
import time


def zero_conds_to_str(zero_conds: List[Condition]) -> str:
    return "Zero condition: %s" % "; ".join(map(str, zero_conds))


def non_zero_conds_to_str(non_zero_conds: List[Condition]) -> str:
    return "Non zero condition: %s" % "; ".join(map(str, non_zero_conds))


def worker(system, input_tasks, done_tasks):
    def append_to_input(x):
        input_tasks.put(x)
        logger.info("AAAAPPPPPPPPPPPPPPPPEND")
    logger.info('[{}.{}] got system \n{}'.format(mp.current_process().name, mp.current_process().pid, system))
    system.open_log_file()
    try:
        system.estimate(append_to_input)
    except Exception as ex:
        logger.info("EEEEEXCCCCCCCCCCCCCCEEEEEEEEEEEEEPPPPPPPPPT {0}".format(type(ex)))
        logger.info("EEEEEXCCCCCCCCCCCCCCEEEEEEEEEEEEEPPPPPPPPPT {0}".format(ex))
        raise ex
    # after get_estimate we should get estimate so we can add the system to done_tasks
    system.close_log_file()
    done_tasks.put(system)
    input_tasks.put('no-task')


def main(transitions, inputs, outputs, amount_workers=mp.cpu_count()):
    logger.info("Basic transitions are: \n{}\n\n".format('\n'.join(map(str, transitions))))

    logger.info("Creating common conditions...")
    ccond_generator = CommonConditionGenerator()
    input_conditions = ccond_generator.gen_all_common_conditions(inputs)
    output_conditions = ccond_generator.gen_all_common_conditions(outputs)

    assert len(input_conditions) == len(output_conditions)

    logger.info("Generating systems...")
    mp_manager = mp.Manager()
    input_tasks = mp_manager.Queue()
    done_tasks = mp_manager.Queue()
    logger.info("Created input_tasks = {}, done_tasks = {}".format(input_tasks, done_tasks))
    for in_zero_conds, in_non_zero_conds in input_conditions:
        for out_zero_conds, out_non_zero_conds in output_conditions:
            logger.info('-' * 50)
            logger.info("Input condition: \n\t{}\n\t{}".format(zero_conds_to_str(in_zero_conds),
                                                               non_zero_conds_to_str(in_non_zero_conds)))
            logger.info("Output condition: \n\t{}\n\t{}".format(zero_conds_to_str(out_zero_conds),
                                                                non_zero_conds_to_str(out_non_zero_conds)))
            system = SystemTransition([tr.copy() for tr in transitions])
            system.set_common_conditions(in_zero_conds, in_non_zero_conds, out_zero_conds, out_non_zero_conds)
            input_tasks.put(system)

    logger.info("Total {} system was generated with basic common conditions".format(input_tasks.qsize()))
    logger.info("Estimating...")
    if amount_workers == 1:
        while input_tasks.qsize() > 0:
            system = input_tasks.get_nowait()
            if system == 'no-task':
                continue
            worker(system, input_tasks, done_tasks)
    else:
        with mp.Pool(processes=amount_workers) as pool:
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


def clone_with_use_oper(var, op):
    tmp = var.clone()
    tmp.apply_lin_oper(op)
    return tmp


if __name__ == "__main__":

    a1 = Variable(TypeVariable.INPUT)
    a2 = Variable(TypeVariable.INPUT)

    b1 = Variable(TypeVariable.UNKNOWN)

    c1 = Variable(TypeVariable.OUTPUT)
    c2 = Variable(TypeVariable.OUTPUT)

    mu = LOMu()
    lmbda = LOLambda()

    trans = [Transition(Side(a1), Side(b1, clone_with_use_oper(a2, mu)), BlockFunction('F', 'p')),
             Transition(Side(a2), Side(c2, clone_with_use_oper(b1, lmbda)), BlockFunction('G', 'q')),
             Transition(Side(b1), Side(c1, clone_with_use_oper(c2, mu)), BlockFunction('F', 'p'))]

    main(trans, [a1, a2], [c1, c2], amount_workers=1)
