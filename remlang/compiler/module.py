from typing import Tuple

from .reference_collections import ReferenceDict
from .token_manager import TokenManager
from .order_dual_opt import op_priority
from ..standard import default
import hashlib

# this is the manager of modules
default_env = ReferenceDict(
    {
        '@modules': {'main': ''},
    })


def make_new_module(name: str, module_manager: 'ReferenceDict', token_manager: 'TokenManager' = None):
    """make a new module
    """
    env = ReferenceDict(default.default, module_manager=module_manager)
    env.update(
        __name__=name,
        OperatorPriority=op_priority,
        __token__=token_manager if token_manager else TokenManager())
    module_manager[name] = env

    env['中文编程'] = lambda: env['__token__'].mut_by(env['cast'](env['to_chinese']))
    default_env[name] = env
    return env


def md5(path, max_size=1024 * 2) -> 'Tuple[str, str]':
    with open(path, 'r') as f:
        src = f.read()
    return src, hashlib.md5(src).hexdigest()
