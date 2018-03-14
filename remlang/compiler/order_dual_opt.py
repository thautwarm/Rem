from .linked_list import RevLinkedList, RevNode
from collections import namedtuple
import operator
from cytoolz import curry

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
    '!=': curry(operator.ne)
}


def order_dual_opt(seq):
    if len(seq) <= 3:
        return seq

    arg_indices = argsort([op_priority[e] for e in seq if isinstance(e, str)])
    arg_indices.reverse()

    indices = [idx for idx, e in enumerate(seq) if isinstance(e, str)]
    indices.reverse()

    linked_list = RevLinkedList.from_iter(seq)
    nodes = []
    node = linked_list.head

    n = indices.pop()
    for i in range(len(seq)):
        if i == n:
            nodes.append(node)
            if indices:
                n = indices.pop()
            else:
                break
        node = node.next

    op_order = [nodes[i] for i in arg_indices]

    for ordered_op in op_order:

        left: RevNode = ordered_op.prev
        right: RevNode = ordered_op.next
        mid: RevNode = ordered_op

        new_node = RevNode(BinExp(left.content, mid.content, right.content))

        if ordered_op.prev.prev is not None:
            ordered_op.prev.prev.next = new_node
            new_node.next = ordered_op.next.next

    return order_dual_opt(linked_list.to_list)

# print(order_dual_opt([1, '+', 2, '*', 3]))
