from typing import Tuple
from Ruikowa.ErrorHandler import ErrorHandler
from .reference_collections import ReferenceDict
from .order_dual_opt import op_priority
from ..standard import default
import hashlib

try:
    from cytoolz import compose
except ModuleNotFoundError:
    from toolz import compose

# this is the manager of modules
default_env = ReferenceDict(
    {
        '@modules': {'main': ''},
    })


def make_new_module(name: str, module_manager: 'ReferenceDict', compiler: 'ErrorHandler' = None):
    """make a new module
    """
    env = ReferenceDict(default.default.copy(), module_manager=module_manager)
    env.update(
        __name__=name,
        OperatorPriority=op_priority,
        __compiler__=compiler)
    module_manager[name] = env

    env['中文编程'] = lambda: env['__compiler__'].mut_token_by(
        lambda origin_func: compose(env['to_chinese'], origin_func))

    default_env[name] = env
    return env


def md5(path) -> 'Tuple[str, str]':
    with open(path, 'r') as f:
        src = f.read()
    return src, hashlib.md5(src.encode()).hexdigest()


class ModuleAgent:
    __slots__ = ['_']

    def __init__(self, module: dict):
        self._ = module

    def __getattr__(self, item):
        try:
            return self._[item]
        except KeyError:
            raise NameError(f'{self._["__name__"]}.{item}')