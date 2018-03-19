from .reference_collections import ReferenceIter
from .rem_parser import UNameEnum, Tokenizer
from Ruikowa.ObjectRegex.ASTDef import Ast
from typing import Union

unmatched = object()
const_map = {'r': True, 'a': False, 'o': None}


def _pattern_match(left_e: Union[Ast, Tokenizer], right_e, ctx):
    try:
        if left_e.name is UNameEnum.refName:

            [*ref, symbol] = left_e
            name = symbol.string
            if ref:
                return ctx.get_nonlocal(name) == right_e
            else:
                ctx.set_local(name, right_e)
                return True

        elif left_e.name is UNameEnum.string:
            return eval(left_e.string) == right_e

        elif left_e.name is UNameEnum.const:
            return const_map[left_e.string[1]] is right_e

        elif left_e.name is UNameEnum.number:
            return eval(left_e.string) == right_e

        elif left_e.name is UNameEnum.tupleArg:
            if not left_e:
                try:
                    next(right_e)
                except StopIteration:
                    return True
                else:
                    return False
            many = left_e[0]
            return pattern_match(many, right_e, ctx)

        elif left_e.string is '_':
            right_e.clear()
            return True
        else:
            assert False

    except:
        return False


def pattern_match(left, right, ctx):
    try:
        is_iter: bool = False
        if left[-1].name is UNameEnum.iterMark:
            left.pop()
            is_iter = True
        elif len(left) > 1:
            is_iter = True

        if not is_iter:
            # no
            return _pattern_match(left[0][-1], right, ctx)

        left = ReferenceIter(left)
        right = ReferenceIter(right)

        while True:
            try:
                k = next(left)
            except StopIteration:
                try:
                    next(right)
                    # no
                    return False
                except StopIteration:
                    # no
                    return True

            else:
                if len(k) is 2:
                    k = k[1]
                    if not _pattern_match(k, right.c, ctx):
                        # no
                        return False
                    return True

                v = next(right)
                if not _pattern_match(k[0], v, ctx):
                    # no
                    return False
    except:
        return False
