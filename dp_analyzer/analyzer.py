#!/usr/bin/python3

from logger import logger
from system_transition import SystemTransition
from condition import Condition, ConditionState
from common_condition_generator import CommonConditionGenerator
from typing import List
import multiprocessing as mp
from os.path import join as path_join
from os import getcwd, makedirs
from data.vars import System
from collector import collector, Node


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


def add_base_system_to_queue(queue, transitions, in_zero_conds, in_non_zero_conds, out_zero_conds, out_non_zero_conds):
    logger.info('-' * 50)
    logger.info("Input condition: \n\t{}\n\t{}".format(zero_conds_to_str(in_zero_conds),
                                                       non_zero_conds_to_str(in_non_zero_conds)))
    logger.info("Output condition: \n\t{}\n\t{}".format(zero_conds_to_str(out_zero_conds),
                                                        non_zero_conds_to_str(out_non_zero_conds)))

    system = SystemTransition([tr.copy() for tr in transitions])
    system.set_common_conditions(in_zero_conds, in_non_zero_conds, out_zero_conds, out_non_zero_conds)
    system.set_node(collector.create_root_node())
    queue.put(system)


def main(transitions, inputs, outputs, cond_func, amount_workers=mp.cpu_count()):
    logger.info("Basic transitions are: \n{}\n\n".format('\n'.join(map(str, transitions))))

    logger.info("Creating common conditions...")
    ccond_generator = CommonConditionGenerator()
    input_conditions = ccond_generator.gen_all_common_conditions(inputs)
    output_conditions = ccond_generator.gen_all_common_conditions(outputs)

    logger.info("Generating systems...")
    mp_manager = mp.Manager()
    input_tasks = mp_manager.Queue()
    done_tasks = mp_manager.Queue()
    logger.info("Created input_tasks = {}, done_tasks = {}".format(input_tasks, done_tasks))
    for in_zero_conds, in_non_zero_conds in input_conditions:
        for out_zero_conds, out_non_zero_conds in output_conditions:
            if cond_func is not None:
                additional_conds = cond_func(out_zero_conds)    # type: List[Condition]
                assert len(additional_conds) > 0
                for add_cond in additional_conds:
                    new_in_zero_conds = [cond.copy() for cond in in_zero_conds]
                    new_in_non_zero_conds = [cond.copy() for cond in in_non_zero_conds]
                    new_out_zero_conds = [cond.copy() for cond in out_zero_conds]
                    new_out_non_zero_conds = [cond.copy() for cond in out_non_zero_conds]
                    if add_cond.get_state() == ConditionState.IS_ZERO:
                        new_out_zero_conds.append(add_cond)
                    else:
                        assert add_cond.get_state() == ConditionState.IS_NOT_ZERO
                        new_out_non_zero_conds.append(add_cond)
                    add_base_system_to_queue(input_tasks, transitions, new_in_zero_conds, new_in_non_zero_conds,
                                             new_out_zero_conds, new_out_non_zero_conds)
            else:

                add_base_system_to_queue(input_tasks, transitions, in_zero_conds, in_non_zero_conds, out_zero_conds, out_non_zero_conds)

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

    logger.info("Results:")
    total_tasks = done_tasks.qsize()
    while done_tasks.qsize() > 0:
        system = done_tasks.get_nowait()    # type: SystemTransition
        system.handle_by_collector()
        logger.info("system-{}: {}".format(system.get_system_id(), system.get_mark()))
    logger.info("Done total tasks - {}".format(total_tasks))
    return total_tasks

if __name__ == "__main__":

    root_log_path = path_join(getcwd(), "logs")
    makedirs(root_log_path, exist_ok=True)
    SystemTransition.set_base_log_path(root_log_path)

    from data.misty import systems, cipher_name

    for amount_rounds in sorted(list(systems.keys())):
        system_log_path = path_join(root_log_path, str(cipher_name), '{}_rounds'.format(amount_rounds))
        makedirs(system_log_path, exist_ok=True)
        SystemTransition.set_base_log_path(system_log_path)
        system = systems[amount_rounds]     # type: System
        total_cases = main(system.transitions, system.inputs, system.outputs, system.output_condition_func, amount_workers=4)
        marks = collector.collect()
        with open(path_join(system_log_path, "marks.txt"), "w") as f_mark:
            f_mark.write("System: \n\n")
            f_mark.write('\n'.join(map(str, system.transitions)))
            f_mark.write("\n\nwhere\n")

            f_mark.write("[{}] - input variables\n".format(', '.join(map(str, system.inputs))))
            f_mark.write("[{}] - output variables\n".format(', '.join(map(str, system.outputs))))
            f_mark.write("b[N] - unknown variables (N = 0;1;2;3...)\n")

            f_mark.write("\nTotal cases handled: {}\n".format(total_cases))

            f_mark.write("\nMarks:\n")
            for mark in marks:
                f_mark.write("\t{}\n".format(mark))
        logger.info("Analyzer done with {} cipher with {} rounds".format(cipher_name, amount_rounds))
