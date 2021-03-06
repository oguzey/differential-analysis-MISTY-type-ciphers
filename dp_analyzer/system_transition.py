from transition import Transition
from condition import Condition, ConditionException, ConditionState
from side import Side
from logger import logger
from typing import List, Callable, Set, Optional
from counter import Counter
import logging
from os.path import join as path_join
from os import rename, getcwd
from sympy import Symbol
import inspect
from collector import collector, Node, NodeType


class SystemTransition(object):
    __id = Counter()
    _base_log_path = path_join(getcwd(), "logs")  # type: str

    @staticmethod
    def set_base_log_path(log_path: str) -> None:
        SystemTransition._base_log_path = log_path

    def __init__(self, transitions: List[Transition]) -> None:
        assert all([isinstance(x, Transition) for x in transitions])
        self.__transitions = transitions  # type: List[Transition]
        self._mark = None  # type: Optional[Symbol]
        self._id = SystemTransition.__id.increment()  # type: int
        # Can not initialize logger here because have serialize issue in multiprocess module.
        # Functions 'open_log_file' and 'close_log_file' should be called before work and after work with object.
        self._logger = None  # type: logging.Logger
        self._file_handler = []  # type: List

        self._is_clone = False

        # Condition variables
        # Unchanged variables
        self._common_zero_conds = None  # type: List[Condition]
        self._common_non_zero_conds = None  # type: List[Condition]

        self._conds_zero = []  # type: List[Condition]
        self._conds_non_zero = []  # type: List[Condition]
        self._conds_equals = []  # type: List[Condition]

        # collecting marks
        self._node = None   # type: Node
        self._nodes = []    # type: List[Node]

    def __str__(self) -> str:
        system = ""  # type: str
        for ind in range(len(self.__transitions)):
            system += "%d) %s\n" % (ind + 1, str(self.__transitions[ind]))
        return system

    def set_node(self, node: Node) -> None:
        assert node is not None and isinstance(node, Node)
        self._node = node

    def handle_by_collector(self) -> None:
        for node in self._nodes:
            collector.append_to_nodes(node)

    def save_node(self, node: Node) -> None:
        self._nodes.append(node)

    def open_log_file(self) -> None:
        self._logger = logging.getLogger("system_transition.new_object")
        fh = logging.FileHandler(path_join(SystemTransition._base_log_path, str(self._id)))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter('%(message)s'))
        self._logger.addHandler(fh)
        self._file_handler.append(fh)

    def close_log_file(self) -> None:
        assert len(self._file_handler) > 0
        for handler in self._file_handler:
            self._logger.removeHandler(handler)
            handler.flush()
            handler.close()
            # rename file with results
            new_name = path_join(SystemTransition._base_log_path, 'case_{}__mark_is_{}'.format(self._id, self._mark))
            rename(handler.baseFilename, new_name)

        self._file_handler.clear()
        self._logger = None

    def get_system_id(self) -> int:
        return self._id

    def get_amount_rounds(self) -> int:
        assert all(not tran.has_both_empty_side() for tran in self.__transitions)
        return len(self.__transitions)

    def get_mark(self) -> Optional[Symbol]:
        return self._mark

    def set_common_conditions(self, in_zero_cond: List[Condition], in_non_zero_cond: List[Condition],
                              out_zero_cond: List[Condition], out_non_zero_cond: List[Condition]) -> None:
        # Set zero conditions
        self._common_zero_conds = []
        self._common_zero_conds.extend(in_zero_cond)
        self._common_zero_conds.extend(out_zero_cond)
        # NOTE: set self._conds_zero in function simplify

        # Set non zero conditions
        self._common_non_zero_conds = []
        self._common_non_zero_conds.extend(in_non_zero_cond)
        self._common_non_zero_conds.extend(out_non_zero_cond)
        self._conds_non_zero = self._common_non_zero_conds[:]

    @staticmethod
    def _conds_to_str(conditions: List[Condition]) -> str:
        return "{{\n\t{}\n}}".format("\n\t".join(map(str, conditions)))

    def dump_system(self, msg: str='', log_fn=None, with_trans=True, with_main_conds=True, with_common_conds=False) -> None:
        if log_fn is None:
            log_fn = self._logger.info
        log_fn('{0} {1} {0}'.format('-'*20, msg))
        if with_trans:
            log_fn('Transitions: \n{}'.format(self))
        if with_main_conds:
            log_fn('Zero conds: {}'.format(self._conds_to_str(self._conds_zero)))
            log_fn('Non zero conds: {}'.format(self._conds_to_str(self._conds_non_zero)))
            log_fn('Equals conds: {}'.format(self._conds_to_str(self._conds_equals)))
        if with_common_conds:
            log_fn('Common zero conditions: {}'.format("; ".join(map(str, self._common_zero_conds))))
            log_fn('Common non zero conditions: {}'.format("; ".join(map(str, self._common_non_zero_conds))))
        log_fn('{0}{0}'.format('-' * 40))

    def __clone(self, is_fork: bool=False) -> 'SystemTransition':

        new_system = SystemTransition([tr.copy() for tr in self.__transitions])
        new_system._is_clone = True

        new_system._common_zero_conds = self._common_zero_conds
        new_system._common_non_zero_conds = self._common_non_zero_conds

        new_system._conds_zero = [cond.copy() for cond in self._conds_zero]
        new_system._conds_non_zero = [cond.copy() for cond in self._conds_non_zero]
        new_system._conds_equals = [cond.copy() for cond in self._conds_equals]

        collector.make_parent_node(self._node, NodeType.FORK if is_fork else NodeType.BRANCH)
        self.save_node(self._node)
        node_child1, node_child2 = collector.create_children(self._node)

        self._node = node_child1
        new_system._node = node_child2

        return new_system

    def __apply_condition(self, condition: Condition) -> None:
        assert isinstance(condition, Condition)
        for transition in self.__transitions:
            transition.apply_condition(condition)

    def _use_and_append_zero_cond(self, condition: Condition) -> None:
        self.__apply_condition(condition)
        self.dump_system("System after apply condition {}".format(condition), with_main_conds=False)
        for nzcondition in self._conds_non_zero:
            if nzcondition.update_with(condition):
                self.dump_system("Conditions after apply condition {}".format(condition), with_trans=False)
            if not nzcondition.is_correct():
                func = inspect.currentframe().f_back.f_code
                raise ConditionException("[{}:{}] Contradiction detected '{}'".format(func.co_name, func.co_firstlineno, nzcondition))

        new_zero_conds = []
        useless_econds = []
        for econdition in self._conds_equals:
            if econdition.update_with(condition):
                self.dump_system("[_use_and_append_zero_cond] Conditions after apply condition {}".format(condition), with_trans=False)
            if not econdition.is_correct():
                func = inspect.currentframe().f_back.f_code
                raise ConditionException("[{}:{}] Contradiction detected '{}'".format(func.co_name, func.co_firstlineno, econdition))
            if econdition.get_state() == ConditionState.IS_ZERO:
                #  condition was converted
                new_zero_conds.append(econdition)
            if econdition.is_useless():
                useless_econds.append(econdition)
                logger.debug("useless: Condition {} true ".format(econdition))
            else:
                logger.debug("useless: Condition {} false ".format(econdition))

        if condition.get_state() == ConditionState.IS_EQUAL:
            self._conds_equals.append(condition)
        else:
            self._conds_zero.append(condition)
        self.dump_system("Added condition {}".format(condition), with_trans=False)
        #  remove useless condition
        if len(useless_econds):
            for ucondition in useless_econds:
                self._conds_equals.remove(ucondition)
                logger.info("_use_and_append_zero_cond: remove useless condition from _conds_equals '{}'".format(ucondition))
            self.dump_system("Clear _conds_equals", with_trans=False)
        # remove and apply new zero conditions
        if len(new_zero_conds) > 0:
            for zcondition in new_zero_conds:
                self._conds_equals.remove(zcondition)
                logger.info("_use_and_append_zero_cond: remove new zero condition from _conds_equals '{}'".format(zcondition))
            self.dump_system("Clear _conds_equals 2", with_trans=False)
            for zcondition in new_zero_conds:
                self._use_and_append_zero_cond(zcondition)

    def _remove_empty_transitions(self) -> int:
        rm = []
        for transition in self.__transitions:
            if transition.has_both_empty_side():
                rm.append(transition)

        for transition in rm:
            self.__transitions.remove(transition)
        return len(rm)

    def _analyse_and_generate_new_conditions(self) -> int:
        null_trans = []

        for transition in self.__transitions:
            assert transition.has_both_empty_side() == False
            if transition.has_empty_side():
                null_trans.append(transition)
                continue

        for transition in null_trans:
            self.__transitions.remove(transition)
            if not transition.has_both_empty_side():
                self._use_and_append_zero_cond(transition.make_zero_condition())

        return len(null_trans)

    def _apply_equals_conditions(self) -> None:
        amount_new_conditions = 1
        while amount_new_conditions > 0:
            for condition in self._conds_equals:
                self.__apply_condition(condition)

            self._remove_empty_transitions()
            amount_new_conditions = self._analyse_and_generate_new_conditions()

    def _is_side_non_zero(self, side: Side) -> bool:
        if len(side) == 1 and side.get_first().is_zero():
            return True
        for nzcondition in self._conds_non_zero:
            assert nzcondition.get_state() == ConditionState.IS_NOT_ZERO
            if nzcondition.get_left_side() == side:
                return True
        return False

    def _generate_new_non_zero_conds(self) -> None:
        for transition in self.__transitions:
            left = transition.get_left_side()
            right = transition.get_right_side()
            if self._is_side_non_zero(left):
                if right.is_empty():
                    func = inspect.currentframe().f_back.f_code
                    raise ConditionException(
                        "[{}:{}] Contradiction detected in '{}'. '{}' != 0 but '{}' = 0"
                            .format(func.co_name, func.co_firstlineno, transition, left, right))
                else:
                    self._conds_non_zero.append(Condition.create_non_zero_condition(right.copy()))
            elif self._is_side_non_zero(right):
                if left.is_empty():
                    func = inspect.currentframe().f_back.f_code
                    raise ConditionException(
                        "[{}:{}] Contradiction detected in '{}'. '{}' != 0 but '{}' = 0"
                            .format(func.co_name, func.co_firstlineno, transition, right, left))
                else:
                    self._conds_non_zero.append(Condition.create_non_zero_condition(left.copy()))

    def estimate(self, append_system_fn: Callable[['SystemTransition'], None]) -> None:
        logger.info("Start with system {}".format(self._id))

        # For debugging
        if self._id == 8:
            logger.info("start debuging")

        try:
            self._simplify()
            self._estimate_internal(append_system_fn)
        except ConditionException as ce:
            logger.info("System has contradiction conditions: {}".format(ce))
            self.dump_system('Meet with contradiction: {}'.format(ce))
            self._mark = None
        finally:
            logger.info("Done with system {}".format(self._id))

    def _simplify(self) -> None:
        if self._is_clone:
            self.dump_system('Simplifying cloned system {}'.format(self._id))
            #  System was cloned from other system
            # if self._parent is not None:
            #     self._parent.dump_system('Parent was', self._logger.info)
        else:
            self.dump_system('Simplifying new system {}'.format(self._id), with_common_conds=True)
            # Apply all zero conditions and drop them as variables became zero

            for condition in self._common_zero_conds:
                self._use_and_append_zero_cond(condition)
            self.dump_system('After applied zero conditions')
            self._generate_new_non_zero_conds()
            self.dump_system('Generated new non zero conditions')

        self._apply_equals_conditions()
        self.dump_system('After applied equals conditions')

    def _estimate_internal(self, append_system_fn: Callable[['SystemTransition'], None]) -> None:
        count_triviality = 0
        count_with_unknowns = 0
        self.dump_system('start estimation')

        some_transitions_removed = True
        while some_transitions_removed:
            logger.debug("Start analyse from last transition")
            some_transitions_removed = False
            for x in range(len(self.__transitions) - 1, -1, -1):
                transition = self.__transitions[x]
                logger.debug("Analyse transition {}".format(transition))
                left = transition.get_left_side()
                right = transition.get_right_side()

                assert len(left) > 0 and len(right) > 0

                # 2 sides does not have unknowns
                if not left.contains_unknown() and not right.contains_unknown():
                    count_triviality += 1
                    logger.debug("Transition {} is triviality".format(transition))
                    continue

                is_left_non_zero = self._is_side_non_zero(left)
                is_right_non_zero = self._is_side_non_zero(right)

                if is_left_non_zero and is_right_non_zero:
                    logger.debug("Both sides '{}' and '{}' are not zero".format(left, right))
                    # do nothing, just increase counter
                    count_with_unknowns += 1
                    continue
                elif is_left_non_zero and not is_right_non_zero:
                    logger.debug("Left side '{}' is NON ZERO. Rigth is undefined '{}'".format(left, right))
                    # fixed left side - not fork
                    nz = Condition.create_non_zero_condition(right.copy())
                    logger.debug("Create non zero condition '{}'".format(nz))
                    self._conds_non_zero.append(nz)
                    count_with_unknowns += 1
                    continue
                elif not is_left_non_zero and is_right_non_zero:
                    logger.debug("Right side '{}' is NON ZERO. Left is undefined '{}'".format(right, left))
                    # fixed right side - not fork
                    nz = Condition.create_non_zero_condition(left.copy())
                    logger.debug("Create non zero condition: '{}'".format(nz))
                    self._conds_non_zero.append(nz)
                    count_with_unknowns += 1
                    continue
                else:
                    fork = False
                    # both sides not zero
                    # check that they does not contain unkwowns
                    if not left.contains_unknown() or not right.contains_unknown():
                        logger.info('Left or right sides does not contains UNKNOWN')
                        # need divide in two cases: zero and not zero
                        # zero case
                    else:
                        logger.info(
                            "Left and right contains UNKNOWN and sides in undefined. 'Fork' will processing")
                        fork = True

                    new_system = self.__clone(is_fork=fork)
                    # create non zero condition and add them to new system
                    # logger.debug("Creating new conditions for non zero case")
                    left_nzc = Condition.create_non_zero_condition(left.copy())
                    right_nzc = Condition.create_non_zero_condition(right.copy())
                    logger.debug("New non zero conditions '{}' and '{}'".format(left_nzc, right_nzc))
                    new_system._conds_non_zero.append(left_nzc)
                    new_system._conds_non_zero.append(right_nzc)
                    append_system_fn(new_system)
                    logger.debug("New system with id {} added to queue".format(new_system._id))

                    # logger.debug("Creating new conditions for zero case")
                    left_zc = Condition.create_zero_condition(left.copy())
                    right_zc = Condition.create_zero_condition(right.copy())
                    logger.debug("New zero conditions '{}' and '{}'".format(left_zc, right_zc))
                    self._use_and_append_zero_cond(left_zc)
                    self._use_and_append_zero_cond(right_zc)
                    some_transitions_removed = False
                    res = 1
                    while res > 0:
                        res = self._remove_empty_transitions()
                        res += self._analyse_and_generate_new_conditions()
                        some_transitions_removed |= bool(res)
                    if some_transitions_removed:
                        break
                    continue

        self._mark = None
        for tr in self.__transitions:
            if self._mark is None:
                self._mark = Symbol(tr.get_probability())
            else:
                self._mark *= Symbol(tr.get_probability())

        N = Symbol('N')
        amount = self._count_special_equal_conds()
        for i in range(amount):
            if self._mark is None:
                self._mark = N
            else:
                self._mark *= N
        if self._mark is not None:
            collector.make_node_leaf(self._node, self._mark)
            self.save_node(self._node)

        self.dump_system('Estimated with mark {}'.format(str(self._mark)))
        return

    def _count_special_equal_conds(self) -> int:
        amount = 0
        for econdition in self._conds_equals:
            left = econdition.get_left_side()
            assert len(left) == 1
            left_var = left.get_first()
            if left_var.is_unknown():
                right = econdition.get_right_side()
                assert len(right) == 1
                right_var = right.get_first()
                if right_var.contains_inverse_lo_lambda():
                    logger.info("_count_special_equal_conds: Found special condition with unknown: {}".format(econdition))
                    amount += 1
        logger.info("_count_special_equal_conds: found {} special equal_conds for sid = {}".format(amount, self._id))
        return amount
