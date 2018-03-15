try:
    from cytoolz import curry
except ModuleNotFoundError:
    from toolz import curry

from functools import reduce
from collections import Iterable, OrderedDict
from ..compiler.utils import cast, to_chinese

LICENSE_INFO = """
Rem Language 0.3.2 alpha, March 15 2018 02:14. 
Backend CPython, Author thautwarm, MIT License.
Report at https://github.com/thautwarm/Rem/issues.
"""


class Object:
    pass


@curry
def open_do(file_name, mode):
    return open(file_name, mode)


@curry
def write(content, f):
    file = f('w')
    with file:
        file.write(content)


@curry
def read(f):
    with f('r') as file:
        return file.read()


def xrange(arg):
    if not isinstance(arg, tuple):
        return range(arg)
    return range(*arg)


@curry
def foreach(collection, f):
    for each in collection:
        f(each)


@curry
def _while(condition, f):
    while condition():
        f()


def indexer(arg):
    if not isinstance(arg, Iterable):
        return slice(arg)

    res = tuple(slice(*e) if isinstance(e, Iterable) else slice(e) for e in arg)
    if len(res) is 1:
        res = res[0]
    return res


@curry
def _slice(collection, arg):
    return collection[indexer(arg)]


default = {
    'list': list,
    'tuple': tuple,
    'hashset': set,
    'dict': dict,
    'odict': OrderedDict,
    'max': max,
    'min': min,
    'print': print,
    'help': help,
    'get': curry(getattr),
    'filter': curry(lambda collection, f: filter(f, collection)),
    'map': curry(lambda collection, f: map(f, collection)),
    'reduce': curry(reduce),
    'fold': curry(lambda collection, f, init: reduce(f, collection, init)),
    'call': lambda f: f(),
    'write': write,
    'read': read,
    'open': open_do,
    'cast': cast,
    'to_chinese': to_chinese,
    'range': xrange,
    'foreach': foreach,
    'while': _while,
    'slice': _slice,
    'indexer': indexer,
    'Object': Object,
    'set': curry(setattr),
    'len': len,
    'isa': curry(isinstance)

}
