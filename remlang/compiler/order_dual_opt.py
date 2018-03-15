from .linked_list import RevLinkedList, RevNode
from collections import namedtuple
import operator
from cytoolz import curry
import linq

BinExp = namedtuple('BinExp', ['left', 'mid', 'right'])

argsort = lambda seq: sorted(range(len(seq)), key=seq.__getitem__)

op_priority = {  # priority
    '|>': 2,
    '@': 3,
    '>': 3,
    '<': 3,
    '>=': 3,
    '<=': 3,
    '==': 3,
    '!=': 3,
    '`in`': 4,
    '`or`': 5,
    '`and`': 6,
    '<-': 7,
    '|': 7,  # union
    '&': 8,  # joint

    '+': 9,
    '-': 9,
    '*': 10,
    '/': 10,

    '//': 10,
    '%': 10,
    '++': 12,
    '--': 12,
    '**': 12,

    '^': 12,
    '^^': 12,
    # begin[bit op]
    '>>': 14,
    '<<': 14,
    '||': 14,

    '&&': 14,
    '`is`': 15,
    # end[bit op]
}

bin_op_fns = {
    '+': curry(operator.add),
    '-': curry(operator.sub),
    '*': curry(operator.mul),
    '/': curry(operator.truediv),
    '//': curry(operator.floordiv),
    '++': curry(operator.concat),
    '--': curry(lambda x, y: [_ for _ in x if _ not in y]),

    '&': curry(operator.and_),
    '`and`': curry(lambda x, y: x and y),

    '|': curry(operator.or_),
    '`or`': curry(lambda a, b: a or b),

    '%': curry(operator.mod),
    '**': curry(operator.pow),
    '>>': curry(operator.lshift),
    '<<': curry(operator.rshift),
    '||': curry(operator.or_),
    '^': curry(operator.xor),
    '<': curry(operator.lt),
    '<=': curry(operator.le),
    '>': curry(operator.gt),
    '>=': curry(operator.ge),
    '==': curry(operator.eq),
    '`is`': curry(operator.is_),
    '!=': curry(operator.ne),
    '`in`': curry(lambda e, collection: e in collection)
}


def found_local_max(seq, f):
    last = 0

    def group_helper(x):
        nonlocal last
        print(last)

        now = f(x)
        temp = last
        last = now
        return now - temp > 0

    return tuple(e[-1] for i, e in linq.Flow(seq).Group(group_helper).Enum().Unboxed() if i % 2 == 0)


def order_dual_opt(seq):
    if len(seq) <= 3:
        return seq

    arg_indices = argsort([op_priority[e] for e in seq if isinstance(e, str)])
    arg_indices.reverse()

    indices = [idx for idx, e in enumerate(seq) if isinstance(e, str)]
    indices.reverse()

    linked_list = RevLinkedList.from_iter(seq)
    op_nodes = sorted((e for e in linked_list if isinstance(e.content, str)), key=lambda x: op_priority[x.content],
                      reverse=True)

    each: RevNode
    for each in op_nodes:
        bin_expr = BinExp(each.prev.content, each.content, each.next.content)
        each.content = bin_expr

        if each.prev.prev:
            each.prev.prev.next = each
        if each.next.next:
            each.next.next.prev = each

    return each.content


# print(order_dual_opt([1, '*', 2, '**', 3, '+', 4, '*', 1]))
