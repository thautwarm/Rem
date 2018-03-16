try:
    from cytoolz import curry
except ModuleNotFoundError:
    from toolz import curry

from functools import reduce
from collections import Iterable, OrderedDict
from ..compiler.utils import cast, to_chinese

from .syntax import *
from .io import *

LICENSE_INFO = """
Rem Language 0.3.2 alpha, March 15 2018 02:14. 
Backend CPython, Author thautwarm, MIT License.
Report at https://github.com/thautwarm/Rem/issues.
"""


class Object:
    pass


def xrange(arg):
    if not isinstance(arg, tuple):
        return range(arg)
    return range(*arg)


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
    'while': rem_while,
    'slice': rem_slice,
    'indexer': indexer,
    'Object': Object,
    'set': curry(setattr),
    'len': len,
    'isa': curry(isinstance),
    'raise': rem_raise,
    'if': rem_if,
    'else': rem_else,
}
