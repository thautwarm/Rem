from .reference_collections import ReferenceIter
from .rem_parser import UNameEnum, Tokenizer
from Ruikowa.ObjectRegex.ASTDef import Ast
from typing import Union

if False:
    from .ast import ast_for_expr


def import_ast_for_expr():
    from .ast import ast_for_expr
    globals()['ast_for_expr'] = ast_for_expr


unmatched = object()
const_map = {'r': True, 'a': False, 'o': None}


def pattern_matching(left_e: Union[Ast, Tokenizer], right_e, ctx):
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

        elif left_e.name is UNameEnum.tuplePat:
            if not left_e:
                try:
                    next(iter(right_e))
                except StopIteration:
                    return True
                else:
                    return False
            many = left_e[0]
            return pattern_match_varargs(many, right_e, ctx)
        elif left_e.name is UNameEnum.dictPat:

            if not left_e:
                return not right_e
            kv_pat_many = left_e[0]

            for expr, [dict_value_pat] in kv_pat_many:
                expr = ast_for_expr(expr, ctx)
                if not pattern_matching(dict_value_pat, right_e[expr], ctx):
                    return False

            return True

        elif left_e.string is '_':
            right_e.clear()
            return True
        else:
            assert False

    except:
        return False


def pattern_match_varargs(left, right, ctx):
    try:
        is_iter: bool = False
        if left[-1].name is UNameEnum.iterMark:
            left.pop()
            is_iter = True
        elif len(left) > 1:
            is_iter = True

        if not is_iter:
            # no
            return pattern_matching(left[0][-1], right, ctx)

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
                    if not pattern_matching(k, right.c, ctx):
                        # no
                        return False
                    return True

                v = next(right)
                if not pattern_matching(k[0], v, ctx):
                    # no
                    return False
    except:
        return False
