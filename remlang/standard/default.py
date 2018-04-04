from .curry import curry

from functools import reduce
from collections import Iterable, OrderedDict, Iterator

from ..compiler.utils import cast, to_chinese
from ..compiler.msg import StatusConstructor, RemStatus

from .syntax import *
from .io import *
from .module import *
from .path import Path
from .collections import *

LICENSE_INFO = """
Rem Language 0.4.0 alpha, March 21 2018 06:47. 
Backend CPython, Author thautwarm, MIT License.
Report at https://github.com/thautwarm/Rem/issues.
"""


class Object:
    pass


default = {
    # syntax
    'err': rem_raise,
    'foreach': foreach,
    'while': rem_while,
    'if': rem_if,
    'else': rem_else,

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
    'set': curry(setattr),

    # collections
    'chunk_by': chunk_by,
    'chunk': chunk,
    'filter': curry(lambda collection, f: filter(f, collection)),
    'map': curry(lambda collection, f: map(f, collection)),
    'reduce': curry(lambda collection, f: reduce(f, collection)),
    'fold': curry(lambda collection, f, init: reduce(f, collection, init)),
    'fst': fst,
    'snd': snd,
    'slice': rem_slice,
    'indexer': indexer,

    # function helper
    'call': lambda f: f(),

    # IO
    'write': write,
    'read': read,
    'open': open_file,
    'cast': cast,
    'to_chinese': to_chinese,
    'range': xrange,
    'append': append,

    'Object': Object,
    "index": curry(lambda x, i: x[i]),

    'len': len,
    'is_inst_of': curry(isinstance),
    'is_type_of': curry(lambda type, inst: isinstance(inst, type)),

    'apply_module': apply_module,
    'path': Path,

    'string': str,
    'int': int,
    'float': float,

    # msg
    'status': StatusConstructor,
    'is_status': lambda _: isinstance(_, RemStatus)

}
