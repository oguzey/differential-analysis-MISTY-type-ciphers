
from side import Side
from side import SideException
from conditions import Condition
from conditions import StateConditions
from conditions import CustomConditions
from conditions import ConditionExeption


class Transition(object):
    def __init__(self, left_side, right_side):
        assert isinstance(left_side, Side) and isinstance(right_side, Side)
        self.__left = left_side
        self.__right = right_side
        # test property, need to review
        self.__is_simple = False

    def __str__(self):
        return "{} ---> {}".format(str(self.__left), str(self.__right))

    def set_simple(self):
        self.__is_simple = True

    def get_simple(self):
        return self.__is_simple

    def check_triviality(self):
        return self.__left.is_trivial() and self.__right.is_trivial()

    def copy(self):
        return Transition(self.__left.copy(), self.__right.copy())

    def apply_condition(self, condition):
        if condition.get_state() == StateConditions.IS_NOT_ZERO:
            return

        condition_left = condition.get_left_side()
        condition_right = condition.get_right_side()
        # if self.__left.contains(condition_left) and (
        #         not condition_right.contains_unknown() or
        #         len(condition_right) == 1):
        if self.__left.contains(condition_left):
            self.__left.replace_in_side(condition_left, condition_right)

        if self.__right.contains(condition_left):
            self.__right.replace_in_side(condition_left, condition_right)

    def has_empty_side(self):
        return self.__left.is_empty() or self.__right.is_empty()

    def has_both_empty_side(self):
        return self.__left.is_empty() and self.__right.is_empty()

    def get_left_side(self):
        return self.__left

    def get_right_side(self):
        return self.__right

    def make_condition(self):

        non_zero_side = None
        if self.__left.is_empty() and not self.__right.is_empty():
            non_zero_side = self.__right
        elif not self.__left.is_empty() and self.__right.is_empty():
            non_zero_side = self.__left
        else:
            raise Exception("One side must be not empty in transition")

        return Condition.create_zero_condition(non_zero_side)


class SystemTransition(object):
    amount_cases = 0

    def __init__(self, *transitions):
        assert all([isinstance(x, Transition) for x in transitions])
        self.__transitions = list(transitions)

    def __str__(self):
        system = ""
        for ind in xrange(len(self.__transitions)):
            system += "%d) %s\n" % (ind + 1, str(self.__transitions[ind]))
        return system

    def __len__(self):
        assert all(not tran.has_both_empty_side() for tran in self.__transitions)
        return len(self.__transitions)

    def get_transitions(self):
        return self.__transitions

    def copy(self):
        transitions = [tr.copy() for tr in self.__transitions]
        return SystemTransition(*transitions)

    def apply_condition(self, condition):
        assert isinstance(condition, Condition)
        for transition in self.__transitions:
            # print "Before transition %s ||| condition %s" % (str(transition), str(condition))
            transition.apply_condition(condition)
            # print "After transition %s ||| condition %s" % (str(transition), str(condition))

    def apply_conditions(self, conditions):
        assert isinstance(conditions, list)
        for condition in conditions:
            self.apply_condition(condition)

    def analyse_and_set_custom_conditions(self, custom_cond):
        count = 0
        null_trans = []
        rm = []
        for transition in self.__transitions:
            if transition.has_both_empty_side():
                # print "will rm == ", transition
                rm.append(transition)
            elif transition.has_empty_side():
                # print "emty == ", transition
                null_trans.append(transition)
                count += 1

        for transition in null_trans:
            self.__transitions.remove(transition)

        map(self.__transitions.remove, rm)

        for trans in null_trans:
            custom_cond.append_condition(trans.make_condition())
        return count

    def apply_custom_conditions(self, custom_conditions):
        for index in xrange(len(custom_conditions) - 1, -1, -1):
            condition = custom_conditions.get_condition(index)
            self.apply_condition(condition)

    def apply_common_condition(self, common_condition):
        zero_conds = common_condition.get_zero_condition()
        for condition in zero_conds:
            self.apply_condition(condition)

    def has_condition(self):
        return any([tr.has_empty_side() for tr in self.__transitions])

    def count_unknown_vars(self):
        unknowns = []
        for trans in self.__transitions:
            unknowns.extend(trans.get_left_side().get_unknowns_id())
            unknowns.extend(trans.get_right_side().get_unknowns_id())
            # print "[count_unknown_vars] transition = %s " % str(trans)
            # print "[count_unknown_vars] %s" % str(unknowns)
        s = set(unknowns)
        # print "[count_unknown_vars] len(%s) = %d" % (str(s), len(s))
        return len(s)

    def do_fast_estimation(self, custom_cond, common_cond_nz):
        nz_sides = [cond.get_left_side() for cond in common_cond_nz]

        count_simple = 0
        for trans in self.__transitions:
            tr_left = trans.get_left_side()
            tr_right = trans.get_right_side()

            # print "Let see on %s" % str(trans)
            # print "List of non zero sides {\n\t%s\n}" % "\n\t".join(map(str, nz_sides))

            if tr_left in nz_sides and tr_right not in nz_sides:
                custom_cond.append_condition(
                    Condition.create_non_zero_condition(tr_right.copy()))
                nz_sides.append(tr_right)
                if tr_right.has_only_one_unknown():
                    trans.set_simple()
                    count_simple += 1
            elif tr_left not in nz_sides and tr_right in nz_sides:
                custom_cond.append_condition(
                    Condition.create_non_zero_condition(tr_left.copy()))
                nz_sides.append(tr_left)
                if tr_left.has_only_one_unknown():
                    trans.set_simple()
                    count_simple += 1

            if not tr_left.contains_unknown() and (
                    not tr_right.contains_unknown()):
                trans.set_simple()
                count_simple += 1

        return count_simple == len(self.__transitions)

    def simplify_with_custom_conditions(self, cust_cond):
        count_add_cc = 1  # by default
        while count_add_cc > 0:
            # print "[simplify] New custom conditions " + str(cust_cond)
            self.apply_custom_conditions(cust_cond)
            # print "[simplify] New system apply_custom_conditions \n" + str(self)
            count_add_cc = self.analyse_and_set_custom_conditions(cust_cond)
            # print "[simplify] New system " + str(self)

    @staticmethod
    def estimate(system, custom_cond, common_in, common_out, comcon_nz, res_list, call_as_fork):
        count_triviality = 0
        count_with_unknowns = 0
        print "#"*50 + "start estimation" + "#"*50
        print "This call of function is %s FORK" % ("" if call_as_fork else "NOT")
        print "Start estimate function with "
        print "system \n%s" % str(system)
        print "and custom_conditions %s\n" % str(custom_cond)

        transitions = system.get_transitions()

        for x in xrange(len(transitions) - 1, -1, -1):
            if custom_cond.exist_contradiction(comcon_nz):
                print "ESTIMATE: CONDITIONS HAVE CONTADICTIONS"
                print "custom_conditions %s\n" % str(custom_cond)
                print "common_in ", str(common_in)
                print "common_out ", str(common_out)
                SystemTransition.__write_result(
                        system, custom_cond, common_in, common_out, count_triviality,
                        count_with_unknowns, res_list, call_as_fork, True)
                return None

            transition = transitions[x]
            print "\nAnalyse transition ", str(transition)
            left = transition.get_left_side()
            right = transition.get_right_side()
            assert len(left) > 0 and len(right) > 0

            # 2 sides does not have unknowns
            if not left.contains_unknown() and not right.contains_unknown():
                count_triviality += 1
                print "Transition is triviality"
                continue

            is_left_non_zero = custom_cond.is_side_non_zero(left)
            is_right_non_zero = custom_cond.is_side_non_zero(right)

            if is_left_non_zero and is_right_non_zero:
                print "Both sides of transition are NOT ZERO"
                # do nothing, just increase counter
                count_with_unknowns += 1
                continue
            elif is_left_non_zero and not is_right_non_zero:
                print "Left side '%s' is NON ZERO. Rigth is undefined" % str(left)
                # fixed left side: not fork
                nz = Condition.create_non_zero_condition(right.copy())
                print "Create non zero condition " + str(nz)
                try:
                    custom_cond.append_condition(nz)
                except ConditionExeption:
                    print "#"*30 + "UNEXPECTED CONDITION EXEPTION" + "#"*30
                    SystemTransition.__write_result(
                        system, custom_cond, common_in, common_out, count_triviality,
                        count_with_unknowns, res_list, call_as_fork, True)
                    return
                print "Updated custom condition is " + str(custom_cond)
                count_with_unknowns += 1
                continue
            elif not is_left_non_zero and is_right_non_zero:
                print "Right side '%s' is NON ZERO. Left undefined" % str(right)
                # fixed right side: not fork
                nz = Condition.create_non_zero_condition(left.copy())
                print "Create non zero condition " + str(nz)
                try:
                    custom_cond.append_condition(nz)
                except ConditionExeption:
                    print "#"*30 + "UNEXPECTED CONDITION EXEPTION" + "#"*30
                    SystemTransition.__write_result(
                        system, custom_cond, common_in, common_out, count_triviality,
                        count_with_unknowns, res_list, call_as_fork, True)
                    return
                print "Updated custom condition is " + str(custom_cond)
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
                    print 'Left or right sides does not contains UNKNOWN'
                    # need divide in two cases: zero and not zero
                    # zero case
                else:
                    print "Left and right contains UNKNOWN and sides in undefined"
                    print "IT IS FOOORKKK!!!!!"
                    fork = True
                    res_list.append("fork")

                print "Creating new components for zero case"
                new_custom_c = custom_cond.copy()
                left_zc = Condition.create_zero_condition(left.copy())
                right_zc = Condition.create_zero_condition(right.copy())
                print "New zero conditions %s and %s" % (str(left_zc), str(right_zc))
                new_system = system.copy()
                print "New system copy \n" + str(new_system)
                try:
                    new_custom_c.append_condition(left_zc)
                    new_custom_c.append_condition(right_zc)
                    new_system.simplify_with_custom_conditions(new_custom_c)
                    print "system after simplify \n" + str(new_system)
                    print "Updated custom conditions " + str(new_custom_c)
                    if new_custom_c.exist_contradiction(comcon_nz):
                        print "ESTIMATE: CONDITIONS HAVE CONTADICTIONS2"
                        print "custom_conditions %s\n" % str(custom_cond)
                        print "common_in ", str(common_in)
                        print "common_out ", str(common_out)
                        SystemTransition.__write_result(
                                new_system, custom_cond, common_in, common_out, count_triviality,
                                count_with_unknowns, res_list, call_as_fork, True)
                        return
                    print "Goto recursion"

                except ConditionExeption:
                    print "#"*30 + "Catche ConditionExeption. System FAIL." + "#"*30
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
                print "New non zero conditions %s and %s" % (str(left_nzc), str(right_nzc))
                try:
                    custom_cond.append_condition(left_nzc)
                    custom_cond.append_condition(right_nzc)
                    print "Updated custom conditions " + str(custom_cond)
                    count_with_unknowns += 1
                except ConditionExeption:
                    print "#"*30 + "Catche ConditionExeption. System FAIL." + "#"*30
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
        print "===>>>BEFORE END<<<==="

        for key, value in dct.items():
            print "%s = %s" % (key, str(value))
        print "===>>>BEFORE END<<<==="
        if was_fail:
            # res_list.append("Fail")
            pass
        else:
            expo = count_triviality + count_with_unknowns - unknown_vars
            est = ("p^%d" % expo, pow(0.5, expo))
            print "current est " + str(est)
            # res_list.append(est)
            if len(res_list) == 0:
                res_list.append(est)
                print "append " + est[0]
            else:
                if res_list[0] == 'fork':
                    res_list.append(est)
                    print "append " + est[0]
                else:
                    # assert len(res_list) == 1
                    print "res_list = " + str(res_list)

                    for x in xrange(len(res_list)):
                        if isinstance(res_list[x], tuple):
                            comp_expo = res_list[x][1]
                            print "compare with est " + str(res_list[x])
                            if est[1] > comp_expo:
                                res_list[x] = est
                                print "replace to " + est[0]
                            else:
                                print "list withou changes"
                            break
                    else:
                        res_list.append(est)
                        print "append " + est[0]
                    print "list %s" + str(res_list)

        if not call_as_fork:
            print "Not fork end"
        else:
            print "Fork end"

        print "#"*50 + "end estimation" + "#"*50
