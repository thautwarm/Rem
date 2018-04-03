from .curry import curry
from collections import Iterable
from ..compiler.msg import StatusConstructor

if_false_status = StatusConstructor('if_false_status')


# if - else
# """
# use if-else expr in the following way
# let res = if {cond} {
#             do_some
#           } .else{
#             do_some
#           }
# """
@curry
def rem_if(cond_fn, if_true_fn):
    if cond_fn():
        return if_true_fn()

    return if_false_status


def rem_else(status):
    if status is if_false_status:
        return lambda else_do: else_do()
    return lambda _: status


# raise syntax
def rem_raise(exp):
    raise exp


# for-each syntax
@curry
def foreach(collection, f):
    for each in collection:
        f(each)


# while
@curry
def rem_while(condition, f):
    while condition():
        f()


# slice
def indexer(arg):
    if not isinstance(arg, Iterable):
        return slice(arg)

    res = tuple(slice(*e) if isinstance(e, Iterable) else slice(e) for e in arg)
    if len(res) is 1:
        res = res[0]
    return res


@curry
def rem_slice(collection, arg):
    return collection[indexer(arg)]
