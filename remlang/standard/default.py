from cytoolz import curry
from functools import reduce
from ..compiler.utils import cast, to_chinese

LICENSE_INFO = """
Rem Language alpha, March 15 2018 02:14. 
Backend CPython, Author thautwarm, MIT License.
Report at https://github.com/thautwarm/Rem/issues.
"""


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


default = {
    'list': list,
    'tuple': tuple,
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
    'to_chinese': to_chinese
}
