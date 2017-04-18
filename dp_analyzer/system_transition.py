from transition import Transition
from conditions import Condition, ConditionException, CustomConditions
from logger import logger
from typing import List
from common_condition_generator import zero_conds_to_str, non_zero_conds_to_str
from enum import Enum


class SystemTransition(object):
    amount_cases = 0

    def __init__(self, *transitions: Transition) -> None:
        assert all([isinstance(x, Transition) for x in transitions])
        self.__transitions = list(transitions)
        self.__amount_rounds = len(self.__transitions)
        self._common_zero_conds = None
        self._common_non_zero_conds = None
        self._is_estimated = None
        self._mark = None

    def __str__(self) -> str:
        system = ""
        for ind in range(len(self.__transitions)):
            system += "%d) %s\n" % (ind + 1, str(self.__transitions[ind]))
        return system

    def __len__(self) -> int:
        assert all(not tran.has_both_empty_side() for tran in self.__transitions)
        return len(self.__transitions)

    def get_mark(self):
        return self._mark

    def set_common_conditions(self, in_zero_cond, in_non_zero_cond, out_zero_cond, out_non_zero_cond):
        self._common_zero_conds = (in_zero_cond, out_zero_cond)
        self._common_non_zero_conds = (in_non_zero_cond, out_non_zero_cond)

    def amount_rounds(self) -> int:
        return self.__amount_rounds

    def get_transitions(self) -> List[Transition]:
        return self.__transitions

    def copy(self) -> 'SystemTransition':
        transitions = [tr.copy() for tr in self.__transitions]
        return SystemTransition(*transitions)

    def apply_condition(self, condition: Condition) -> None:
        assert isinstance(condition, Condition)
        for transition in self.__transitions:
            # logger.debug("Before transition %s ||| condition %s" % (str(transition), str(condition))
            transition.apply_condition(condition)
            # logger.debug("After transition %s ||| condition %s" % (str(transition), str(condition))

    def apply_conditions(self, conditions: List[Condition]) -> None:
        assert isinstance(conditions, list)
        for condition in conditions:
            self.apply_condition(condition)

    def analyse_and_set_custom_conditions(self, custom_cond):
        count = 0
        null_trans = []
        rm = []
        for transition in self.__transitions:
            if transition.has_both_empty_side():
                # logger.debug("will rm == ", transition
                rm.append(transition)
            elif transition.has_empty_side():
                # logger.debug("emty == ", transition
                null_trans.append(transition)
                count += 1

        for transition in null_trans:
            self.__transitions.remove(transition)

        map(self.__transitions.remove, rm)

        for trans in null_trans:
            custom_cond.append_condition(trans.make_condition())
        return count

    def apply_custom_conditions(self, custom_conditions):
        for index in range(len(custom_conditions) - 1, -1, -1):
            condition = custom_conditions.get_condition(index)
            self.apply_condition(condition)

    def has_condition(self):
        return any([tr.has_empty_side() for tr in self.__transitions])

    def count_unknown_vars(self):
        unknowns = []
        for trans in self.__transitions:
            unknowns.extend(trans.get_left_side().get_unknowns_id())
            unknowns.extend(trans.get_right_side().get_unknowns_id())
            # logger.debug("[count_unknown_vars] transition = %s " % str(trans)
            # logger.debug("[count_unknown_vars] %s" % str(unknowns)
        s = set(unknowns)
        # logger.debug("[count_unknown_vars] len(%s) = %d" % (str(s), len(s))
        return len(s)

    def do_fast_estimation(self, custom_cond, common_cond_nz):
        nz_sides = [cond.get_left_side() for cond in common_cond_nz]

        count_simple = 0
        for trans in self.__transitions:
            tr_left = trans.get_left_side()
            tr_right = trans.get_right_side()

            # logger.debug("Let see on %s" % str(trans)
            # logger.debug("List of non zero sides {\n\t%s\n}" % "\n\t".join(map(str, nz_sides))

            if tr_left in nz_sides and tr_right not in nz_sides:
                custom_cond.append_condition(
                    Condition.create_non_zero_condition(tr_right.copy()))
                nz_sides.append(tr_right)
                if tr_right.has_only_one_unknown():
                    trans.make_simple()
                    count_simple += 1
            elif tr_left not in nz_sides and tr_right in nz_sides:
                custom_cond.append_condition(
                    Condition.create_non_zero_condition(tr_left.copy()))
                nz_sides.append(tr_left)
                if tr_left.has_only_one_unknown():
                    trans.make_simple()
                    count_simple += 1

            if not tr_left.contains_unknown() and (
                    not tr_right.contains_unknown()):
                trans.make_simple()
                count_simple += 1

        return count_simple == len(self.__transitions)

    def simplify_with_custom_conditions(self, cust_cond):
        count_add_cc = 1  # by default
        while count_add_cc > 0:
            # logger.debug("[simplify] New custom conditions " + str(cust_cond)
            self.apply_custom_conditions(cust_cond)
            # logger.debug("[simplify] New system apply_custom_conditions \n" + str(self)
            count_add_cc = self.analyse_and_set_custom_conditions(cust_cond)
            # logger.debug("[simplify] New system " + str(self)

    @staticmethod
    def estimate(system, custom_cond, common_in, common_out, comcon_nz, res_list, call_as_fork):
        count_triviality = 0
        count_with_unknowns = 0
        logger.debug("#"*50 + "start estimation" + "#"*50)
        logger.debug("This call of function is %s FORK" % ("" if call_as_fork else "NOT"))
        logger.debug("Start estimate function with ")
        logger.debug("system \n%s" % str(system))
        logger.debug("and custom_conditions %s\n" % str(custom_cond))

        transitions = system.get_transitions()

        for x in range(len(transitions) - 1, -1, -1):
            if custom_cond.exist_contradiction(comcon_nz):
                logger.debug("ESTIMATE: CONDITIONS HAVE CONTADICTIONS")
                logger.debug("custom_conditions %s\n" % str(custom_cond))
                logger.debug("common_in ", str(common_in))
                logger.debug("common_out ", str(common_out))
                SystemTransition.__write_result(
                        system, custom_cond, common_in, common_out, count_triviality,
                        count_with_unknowns, res_list, call_as_fork, True)
                return None

            transition = transitions[x]
            logger.debug("\nAnalyse transition {}".format(transition))
            left = transition.get_left_side()
            right = transition.get_right_side()
            # TODO: DO NOT INCLUDE ESTIMATION FOR THAT TRANSITION
            #assert len(left) > 0 and len(right) > 0

            # 2 sides does not have unknowns
            if not left.contains_unknown() and not right.contains_unknown():
                count_triviality += 1
                logger.debug("Transition is triviality")
                continue

            is_left_non_zero = custom_cond.is_side_non_zero(left)
            is_right_non_zero = custom_cond.is_side_non_zero(right)

            if is_left_non_zero and is_right_non_zero:
                logger.debug("Both sides of transition are NOT ZERO")
                # do nothing, just increase counter
                count_with_unknowns += 1
                continue
            elif is_left_non_zero and not is_right_non_zero:
                logger.debug("Left side '%s' is NON ZERO. Rigth is undefined" % str(left))
                # fixed left side: not fork
                nz = Condition.create_non_zero_condition(right.copy())
                logger.debug("Create non zero condition " + str(nz))
                try:
                    custom_cond.append_condition(nz)
                except ConditionException:
                    logger.debug("#"*30 + "UNEXPECTED CONDITION EXEPTION" + "#"*30)
                    SystemTransition.__write_result(
                        system, custom_cond, common_in, common_out, count_triviality,
                        count_with_unknowns, res_list, call_as_fork, True)
                    return
                logger.debug("Updated custom condition is " + str(custom_cond))
                count_with_unknowns += 1
                continue
            elif not is_left_non_zero and is_right_non_zero:
                logger.debug("Right side '%s' is NON ZERO. Left undefined" % str(right))
                # fixed right side: not fork
                nz = Condition.create_non_zero_condition(left.copy())
                logger.debug("Create non zero condition " + str(nz))
                try:
                    custom_cond.append_condition(nz)
                except ConditionException:
                    logger.debug("#"*30 + "UNEXPECTED CONDITION EXEPTION" + "#"*30)
                    SystemTransition.__write_result(
                        system, custom_cond, common_in, common_out, count_triviality,
                        count_with_unknowns, res_list, call_as_fork, True)
                    return
                logger.debug("Updated custom condition is " + str(custom_cond))
                count_with_unknowns += 1
                continue
            else:
                new_res_list = []
                res_list.append(new_res_list)
                res_list = new_res_list
                fork = False
                # both sides not zero
                # check that they does not contain unkwowns
                if not left.contains_unknown() or not right.contains_unknown():
                    logger.debug('Left or right sides does not contains UNKNOWN')
                    # need divide in two cases: zero and not zero
                    # zero case
                else:
                    logger.debug("Left and right contains UNKNOWN and sides in undefined")
                    logger.debug("IT IS FOOORKKK!!!!!")
                    fork = True
                    res_list.append("fork")

                logger.debug("Creating new components for zero case")
                new_custom_c = custom_cond.copy()
                left_zc = Condition.create_zero_condition(left.copy())
                right_zc = Condition.create_zero_condition(right.copy())
                logger.debug("New zero conditions %s and %s" % (str(left_zc), str(right_zc)))
                new_system = system.copy()
                logger.debug("New system copy \n" + str(new_system))
                try:
                    new_custom_c.append_condition(left_zc)
                    new_custom_c.append_condition(right_zc)
                    new_system.simplify_with_custom_conditions(new_custom_c)
                    logger.debug("system after simplify \n" + str(new_system))
                    logger.debug("Updated custom conditions " + str(new_custom_c))
                    if new_custom_c.exist_contradiction(comcon_nz):
                        logger.debug("ESTIMATE: CONDITIONS HAVE CONTADICTIONS2")
                        logger.debug("custom_conditions %s\n" % str(custom_cond))
                        logger.debug("common_in ", str(common_in))
                        logger.debug("common_out ", str(common_out))
                        SystemTransition.__write_result(
                                new_system, custom_cond, common_in, common_out, count_triviality,
                                count_with_unknowns, res_list, call_as_fork, True)
                        return
                    logger.debug("Goto recursion")

                except ConditionException:
                    logger.debug("#"*30 + "Catche ConditionExeption. System FAIL." + "#"*30)
                    SystemTransition.__write_result(
                        new_system, custom_cond, common_in, common_out, count_triviality,
                        count_with_unknowns, res_list, call_as_fork, True)
                else:
                    if not fork:
                        SystemTransition.estimate(
                            new_system, new_custom_c, common_in, common_out,
                            comcon_nz, res_list, False)
                    else:
                        # fork
                        SystemTransition.estimate(
                            new_system, new_custom_c, common_in, common_out,
                            comcon_nz, res_list, True)

                # none zero case
                left_nzc = Condition.create_non_zero_condition(left.copy())
                right_nzc = Condition.create_non_zero_condition(right.copy())
                logger.debug("New non zero conditions %s and %s" % (str(left_nzc), str(right_nzc)))
                try:
                    custom_cond.append_condition(left_nzc)
                    custom_cond.append_condition(right_nzc)
                    logger.debug("Updated custom conditions " + str(custom_cond))
                    count_with_unknowns += 1
                except ConditionException:
                    logger.debug("#"*30 + "Catche ConditionExeption. System FAIL." + "#"*30)
                    SystemTransition.__write_result(
                        system, custom_cond, common_in, common_out, count_triviality,
                        count_with_unknowns, res_list, call_as_fork, True)
                    return

                continue

        SystemTransition.__write_result(system, custom_cond, common_in,
                                        common_out, count_triviality, count_with_unknowns,
                                        res_list, call_as_fork, False)

    @staticmethod
    def __write_result(
            system,
            custom_cond,
            common_in,
            common_out,
            count_triviality,
            count_with_unknowns,
            res_list,
            call_as_fork,
            was_fail
            ):

        SystemTransition.amount_cases += 1

        unknown_vars = system.count_unknown_vars()
        dct = {
            "system": system,
            "custom_conditions": custom_cond,
            "common_in": common_in,
            "common_out": common_out,
            "count_unknown_vars": unknown_vars,
            "transition_triviality": count_triviality,
            "transition_with_unknowns": count_with_unknowns,
            "fail": was_fail
        }
        logger.debug("===>>>BEFORE END<<<===")

        for key, value in dct.items():
            logger.debug("%s = %s" % (key, str(value)))
        logger.debug("===>>>BEFORE END<<<===")
        if was_fail:
            # res_list.append("Fail")
            pass
        else:
            expo = count_triviality + count_with_unknowns - unknown_vars
            est = ("p^%d" % expo, pow(0.5, expo))
            logger.debug("current est " + str(est))
            # res_list.append(est)
            if len(res_list) == 0:
                res_list.append(est)
                logger.debug("append " + est[0])
            else:
                if res_list[0] == 'fork':
                    res_list.append(est)
                    logger.debug("append " + est[0])
                else:
                    # assert len(res_list) == 1
                    logger.debug("res_list = " + str(res_list))

                    for x in range(len(res_list)):
                        if isinstance(res_list[x], tuple):
                            comp_expo = res_list[x][1]
                            logger.debug("compare with est " + str(res_list[x]))
                            if est[1] > comp_expo:
                                res_list[x] = est
                                logger.debug("replace to " + est[0])
                            else:
                                logger.debug("list withou changes")
                            break
                    else:
                        res_list.append(est)
                        logger.debug("append " + est[0])
                    logger.debug("list %s" + str(res_list))

        if not call_as_fork:
            logger.debug("Not fork end")
        else:
            logger.debug("Fork end")

        logger.debug("#"*50 + "end estimation" + "#"*50)

    def get_estimate(self):
        logger.debug("=" * 50 + "start" + "=" * 50)
        # Apply all zero conditions and drop them as variables became zero
        in_zero_conds, out_zero_conds = self._common_zero_conds
        for x in in_zero_conds:
            self.apply_condition(x)
        for x in out_zero_conds:
            self.apply_condition(x)

        logger.info("after apply conditions: \n{}".format(self))
        custom_cond = CustomConditions()
        self.simplify_with_custom_conditions(custom_cond)
        logger.info("after system analyze: \n{}".format(self))
        logger.info("all custom conditions: {}".format(custom_cond))

        in_non_zero_conds, out_non_zero_conds = self._common_non_zero_conds
        common_non_zero_conds = list(in_non_zero_conds)
        common_non_zero_conds.extend(out_non_zero_conds)

        logger.info("Input condition: \n\t{}\n\t{}".format(zero_conds_to_str(in_zero_conds),
                                                           non_zero_conds_to_str(in_non_zero_conds)))
        logger.info("Output condition: \n\t{}\n\t{}".format(zero_conds_to_str(out_zero_conds),
                                                            non_zero_conds_to_str(out_non_zero_conds)))

        if custom_cond.exist_contradiction(common_non_zero_conds):
            logger.info("New system has contradiction conditions.")
            logger.debug("FAIL SYSTEM!!!!")
            self._is_estimated = False
            self._mark = None
        elif self.do_fast_estimation(custom_cond, common_non_zero_conds):
            logger.info("CAN BE ESTIMATED  p^%d!!! All primitive transitions" % len(self))
            self._is_estimated = True
            self._mark = ("p^%d" % len(self), pow(0.5, len(self)))
        else:
            logger.info("all custom conditions: {}".format(custom_cond))
            logger.info("after applying conditions: \n{}".format(self))
            logger.debug("=" * 50 + "end" + "=" * 50)
            # SystemTransition.estimate(
            #     self, custom_cond, (in_zero_conds, in_non_zero_conds), (out_zero_conds, out_non_zero_conds),
            #     common_non_zero_conds, case_results, False)