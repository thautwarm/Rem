from cytoolz import curry
from functools import reduce

LICENSE_INFO = """
Rem Language alpha, March 15 2018 02:14. 
Backend CPython, Author thautwarm, MIT License.
Report at https://github.com/thautwarm/Rem/issues.
"""

default = {
    'list': list,
    'tuple': tuple,
    'max': max,
    'min': min,
    'print': print,
    'help': help,
    'get': curry(getattr),
    'filter': curry(filter),
    'map': curry(map),
    'reduce': curry(reduce),
    'fold': curry(lambda f, collection, init: reduce(f, collection, init)),
    'call': lambda f: f()
}
