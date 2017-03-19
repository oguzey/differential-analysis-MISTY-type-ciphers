import copy


def contains_only_str(lst):
    return all(isinstance(elem, str) for elem in lst)


def contains_only_tuples(lst):
    return all(isinstance(elem, tuple) for elem in lst)


def contains_list(lst):
    return any(isinstance(elem, list) for elem in lst)


def remove_empty_str(lst):
    while '' in lst:
        lst.remove('')


def is_empty_fork(lst):
    return len(lst) == 1 and lst[0] == 'fork'


def is_fork_list(lst):
    # print "call is_fork_list with " + str(lst)
    if lst[0] == 'fork':
        # print "first fork"
        for x in xrange(1, len(lst)):
            if not isinstance(lst[x], tuple):
                # print "%s not tup" % str(lst[x])
                return False
        return True
    #  print "do not found fork"
    return False


def get_max_from_tuples(lst):
    assert len(lst) > 0 and contains_only_tuples(lst)
    max_val = lst[0]

    for tup in lst:
        if tup[1] > max_val[1]:
            max_val = tup

    return max_val


def cutted_tuples(lst):
    if len(lst) == 1:
        return lst
    # print "[cutted_tuples] lst = " + str(lst)
    res = [elem for elem in lst if len(elem[0]) <= 4]
    if len(res) == 0:
        return lst
    for elem in res:
        lst.remove(elem)

    # print "[cutted_tuples] res = " + str(res)
    lst.append(get_max_from_tuples(res))
    # print "[cutted_tuples] fin" + str(lst)
    return lst


def get_sum(lst):
    assert not is_empty_fork(lst)
    assert lst[0] == 'fork'

    res_str = ''
    res_value = 0
    for x in xrange(1, len(lst)):
        tup = lst[x]
        res_str += " + " + tup[0]
        res_value += tup[1]

    return (res_str[3:], res_value)


def merge_fork(lst):
    remove_empty_str(lst)
    for x in xrange(len(lst)):
        if isinstance(lst[x], list):
            # print "found list " + str(lst[x])
            remove_empty_str(lst[x])
            if len(lst[x]) == 0 or is_empty_fork(lst[x]):
                lst[x] = ''
                # print "found epty " + str(lst[x])
            elif is_fork_list(lst[x]):
                # print "found fork " + str(lst[x])
                lst[x] = get_sum(lst[x])
            else:
                # print "goto rec with " + str(lst[x])
                merge_fork(lst[x])


def choose_max(array, root, lst):
    remove_empty_str(lst)
    for x in xrange(len(lst)):
        if isinstance(lst[x], list):
            remove_empty_str(lst[x])
            if len(lst[x]) == 0:
                lst[x] = ''
            elif contains_only_tuples(lst[x]):
                copy_lst = cutted_tuples(lst[x])
                # print "list cont tuples " + str(copy_lst)
                # lst[x] = get_max_from_tuples(lst[x])
                for i in xrange(len(copy_lst) - 1):  # do not include self
                    tup = copy_lst[i]
                    lst[x] = tup
                    # print "lst[x] = " + str(lst[x])
                    # print "copy root " + str(root)
                    array.append(copy.deepcopy(root))
                tup = copy_lst[-1]
                lst[x] = tup
            else:
                choose_max(array, root, lst[x])


def get_normalise_result(lst):
    # assert len(lst) != 0
    # while len(lst) == 1:
    #     lst = lst[0]
    # print "input lst " + str(lst)
    array = [lst]
    while any(contains_list(elem) for elem in array):
        for est in array:
            # print "="*50 + "new iteration" + "="*50
            choose_max(array, est, est)
            # print "af choose_max = " + str(lst)
            merge_fork(est)
            # print "af merge_fork = " + str(lst)
            # print "="*50 + "new iteration end" + "="*50
    res = []
    # print "res  = " + str(res)
    for x in array:
        res.extend(x)
    return res


def normalise_polinom(polinom):
    res = polinom.split(' + ')
    while '' in res:
        res.remove('')

    length = len(res)
    if length == 0:
        return ''
    elif length == 1:
        return res[0]
    else:
        # print "[collect_estimates] res = " + str(res)
        new_res = sorted(res, key=lambda est: int(est[2]), reverse=False)
        # print "sorted " + str(new_res)
        final_str = ''
        while len(new_res) > 0:
            elem = new_res.pop(0)
            count = new_res.count(elem) + 1
            final_str += " + %d*%s" % (count, elem)
            while len(new_res) > 0 and new_res[0] == elem:
                new_res.pop(0)
        final_str = final_str[3:]
        # print "in siplify form = " + final_str
        return final_str


def put_normalise_to_dict(data, dct, num_case):
    arr = get_normalise_result(data)
    # print "[put_normalise_to_dict] got " + str(arr)
    while '' in arr:
        arr.remove('')
    for x in arr:
        if not isinstance(x, tuple):
            print "UNEXPECTED DATA " + str(x)
            continue
        pol = normalise_polinom(x[0])
        # print "put %s" % pol
        dct[pol] = num_case


# test = [[[[[('p^0', 1.0), ['fork', [('p^4', 0.0625), [('p^5', 0.03125), [('p^6', 0.015625), [('p^6', 0.015625), [('p^6', 0.015625)]]]]], ['fork', [('p^4', 0.0625)], [['fork', ('p^5', 0.03125), [('p^4', 0.0625)]], [['fork', ('p^6', 0.015625), [('p^5', 0.03125)]], ['fork', [('p^6', 0.015625)], ['fork', ('p^6', 0.015625), [('p^5', 0.03125)]]]]]]]], ['fork', ['fork', ('p^6', 0.015625), [['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], [['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], [['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]]]]], ['fork', [[('p^5', 0.03125)], [['fork', ('p^5', 0.03125), [('p^6', 0.015625)]], ['fork', ('p^6', 0.015625), ['fork', ('p^7', 0.0078125), [('p^6', 0.015625), [('p^6', 0.015625)]]]]]], ['fork', ['fork', [('p^5', 0.03125)], ['fork', ('p^6', 0.015625), [('p^5', 0.03125)]]], [['fork', ['fork', ('p^6', 0.015625), [('p^5', 0.03125)]], ['fork', ['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], ['fork', ('p^6', 0.015625), [('p^5', 0.03125)]]]], ['fork', ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]], ['fork', ['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], ['fork', ('p^6', 0.015625), [('p^5', 0.03125)]]]]]]]]], ['fork', [[[('p^6', 0.015625), [('p^4', 0.0625), [('p^5', 0.03125), [('p^6', 0.015625), [('p^6', 0.015625)]]]]], ['fork', ('p^7', 0.0078125), [['fork', ('p^5', 0.03125), [('p^6', 0.015625)]], [['fork', ('p^5', 0.03125), [('p^5', 0.03125)]], [['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]]]]]], ['fork', [('p^7', 0.0078125), [('p^7', 0.0078125), [('p^7', 0.0078125), [('p^7', 0.0078125), [('p^7', 0.0078125), [('p^7', 0.0078125)]]]]]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], [['fork', ['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]], [['fork', ['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]]]]]]], ['fork', [[[('p^6', 0.015625)], ['fork', ('p^7', 0.0078125), ['fork', ('p^7', 0.0078125), [('p^5', 0.03125), [('p^6', 0.015625), [('p^6', 0.015625)]]]]]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], [['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]]]]]], ['fork', [['fork', [('p^6', 0.015625)], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125), [('p^7', 0.0078125)]]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625), [('p^6', 0.015625)]]]]]], ['fork', ['fork', ['fork', [('p^6', 0.015625)], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]]], ['fork', ['fork', ['fork', [('p^6', 0.015625)], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]]], ['fork', ['fork', ['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]], ['fork', ['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], ['fork', ('p^6', 0.015625), [('p^5', 0.03125)]]]]]]]]]], ['fork', [[['fork', ('p^7', 0.0078125), [[('p^4', 0.0625)], [[('p^5', 0.03125)], [[('p^6', 0.015625)], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]]]]], ['fork', [('p^6', 0.015625), [('p^7', 0.0078125), [('p^7', 0.0078125), [('p^7', 0.0078125), [('p^7', 0.0078125)]]]]], ['fork', ['fork', ('p^6', 0.015625), [('p^7', 0.0078125)]], [['fork', [('p^5', 0.03125)], ['fork', ('p^6', 0.015625), [('p^5', 0.03125)]]], [['fork', [('p^6', 0.015625)], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]], ['fork', [('p^7', 0.0078125)], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]]]]]]], ['fork', [[('p^7', 0.0078125), [('p^7', 0.0078125), [('p^7', 0.0078125), [('p^6', 0.015625), [('p^7', 0.0078125), [('p^7', 0.0078125)]]]]]], ['fork', ('p^8', 0.00390625), [['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], [['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], [['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^8', 0.00390625), [('p^7', 0.0078125)]]]]]]], ['fork', [['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], [['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^8', 0.00390625), ['fork', ('p^8', 0.00390625), [('p^7', 0.0078125), [('p^7', 0.0078125)]]]]]], ['fork', ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^8', 0.00390625), [('p^7', 0.0078125)]]], [['fork', ['fork', [('p^6', 0.015625)], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]]], ['fork', ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^8', 0.00390625), [('p^7', 0.0078125)]]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]]]]]]]], ['fork', [[['fork', ('p^7', 0.0078125), [('p^4', 0.0625), [('p^5', 0.03125), [('p^6', 0.015625), [('p^6', 0.015625)]]]]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ['fork', ('p^6', 0.015625), [('p^7', 0.0078125)]], [['fork', ('p^5', 0.03125), [('p^5', 0.03125)]], [['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]]]]]], ['fork', ['fork', ('p^8', 0.00390625), ['fork', ('p^8', 0.00390625), [('p^7', 0.0078125), [('p^7', 0.0078125), [('p^7', 0.0078125), [('p^7', 0.0078125)]]]]]], ['fork', [['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', [('p^7', 0.0078125)], ['fork', ('p^8', 0.00390625), [('p^7', 0.0078125)]]]], ['fork', ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^8', 0.00390625), [('p^7', 0.0078125)]]], [['fork', ['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]]]]]]], ['fork', [['fork', [('p^7', 0.0078125)], ['fork', [('p^6', 0.015625), [('p^7', 0.0078125), [('p^7', 0.0078125)]]], ['fork', ('p^7', 0.0078125), [('p^5', 0.03125), [('p^6', 0.015625), [('p^6', 0.015625)]]]]]], ['fork', ['fork', ('p^8', 0.00390625), [['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]]]], ['fork', ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], [['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^8', 0.00390625), [('p^7', 0.0078125)]]]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], [['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]]]]]], ['fork', ['fork', ['fork', [('p^7', 0.0078125)], ['fork', ('p^8', 0.00390625), [('p^7', 0.0078125)]]], ['fork', ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125), [('p^7', 0.0078125)]]], ['fork', ('p^8', 0.00390625), [('p^7', 0.0078125), [('p^7', 0.0078125)]]]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125), [('p^7', 0.0078125)]]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625), [('p^6', 0.015625)]]]]]], ['fork', ['fork', ['fork', [('p^7', 0.0078125)], ['fork', ('p^8', 0.00390625), [('p^7', 0.0078125)]]], ['fork', ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^8', 0.00390625), [('p^7', 0.0078125)]]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]]]], ['fork', ['fork', ['fork', [('p^6', 0.015625)], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]], ['fork', ['fork', ('p^7', 0.0078125), [('p^7', 0.0078125)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]]], ['fork', ['fork', ['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], ['fork', ('p^7', 0.0078125), [('p^6', 0.015625)]]], ['fork', ['fork', ('p^6', 0.015625), [('p^6', 0.015625)]], ['fork', ('p^6', 0.015625), [('p^5', 0.03125)]]]]]]]]]]]]
# test2 = [['fork', ['fork', ['fork', ('p^6', 0.015625), [[('p^5', 0.03125)], ['fork', ('p^6', 0.015625), [('p^5', 0.03125)]]]], ['fork', ['fork', ('p^6', 0.015625), []], ['fork', ['fork', ('p^6', 0.015625), [('p^5', 0.03125)]], ['fork', [('p^5', 0.03125)], ['fork', ('p^5', 0.03125), [('p^4', 0.0625)]]]]]], ['fork', ['fork', [[('p^5', 0.03125)], ['fork', ('p^6', 0.015625), [('p^5', 0.03125)]]], ['fork', [('p^5', 0.03125)], ['fork', [('p^5', 0.03125)], ['fork', ('p^5', 0.03125), [('p^4', 0.0625)]]]]], ['fork', ['fork', ['fork', ('p^6', 0.015625), [('p^5', 0.03125)]], ['fork', [('p^5', 0.03125)], ['fork', ('p^5', 0.03125), [('p^4', 0.0625)]]]], ['fork', ['fork', [('p^5', 0.03125)], ['fork', ('p^5', 0.03125), [('p^4', 0.0625)]]], ['fork', ['fork', ('p^5', 0.03125), [('p^4', 0.0625)]], ['fork', [('p^4', 0.0625)], ['fork', ('p^4', 0.0625), [('p^3', 0.125)]]]]]]]]]
# dct = {}

# put_normalise_to_dict(test, dct, 1)
