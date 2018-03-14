from cytoolz import curry
from functools import reduce

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
    'filter': curry(filter),
    'map': curry(map),
    'reduce': curry(reduce),
    'fold': curry(lambda f, collection, init: reduce(f, collection, init)),
    'call': lambda f: f(),
    'write': write,
    'read': read,
    'open': open_do
}
