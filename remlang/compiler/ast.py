import itertools
from collections import Iterable
from functools import reduce
from typing import Optional

from Ruikowa.Bootstrap import Ast
from Ruikowa.ErrorFamily import handle_error
from Ruikowa.ObjectRegex.MetaInfo import MetaInfo

from .reference_collections import ReferenceDict, ReferenceIter
from .order_dual_opt import order_dual_opt, BinExp, bin_op_fns, op_priority
from .rem_parser import file
from ..standard import default
from .token_manager import TokenManager


def flatten(seq):
    for each in seq:
        if isinstance(each, Iterable) and not isinstance(each, str):
            yield from flatten(each)
        else:
            yield each


rem_parser = handle_error(file)

default_env = ReferenceDict(
    {
        '@modules': {'main'},
    })
main = ReferenceDict(
    {
        **default.default,
        'OperatorPriority': op_priority,
        '__name__': 'main',
        '__token__': TokenManager(),
        '@module_manager': default_env,
    },
    module_manager=default_env)

default_env['main'] = main

main['eval'] = lambda src: ast_for_file(rem_parser(main['__token__'](src),
                                                   meta=MetaInfo(),
                                                   partial=False),
                                        main)

main['中文编程'] = lambda: main['__token__'].mut_by(main['cast'](main['to_chinese']))


class RefName:
    def __init__(self, name):
        self.name = name


class BreakUntil:
    __slots__ = ['name']

    def __init__(self, name):
        self.name = name


def ast_for_statements(statements: Ast, ctx: ReferenceDict) -> Optional:
    res = None
    for each in statements:
        res = ast_for_statement(each, ctx)
        if isinstance(res, BreakUntil) and ctx.get_local('@label') != res:
            return res
    return res


def ast_for_statement(statement: Ast, ctx: ReferenceDict) -> Optional:
    sexpr = statement[0]

    if sexpr.name == 'expr':
        if len(statement) is 2:
            res = ast_for_expr(sexpr, ctx)
            if isinstance(res, BreakUntil) and ctx.get_local('@label') != res:
                return res

        else:
            res = ast_for_expr(sexpr, ctx)
            if isinstance(res, BreakUntil) and ctx.get_local('@label') != res:
                return res
            return res

    elif sexpr.name == 'let':
        to_new_ctx = False

        if isinstance(sexpr[0], str):
            to_new_ctx = True
            sexpr = sexpr[1:]

        (name,), *trailers, expr = sexpr
        res = ast_for_expr(expr, ctx)
        if isinstance(res, BreakUntil) and ctx.get_local('@label') != res:
            return res

        if not trailers:

            if to_new_ctx or name in ctx:
                ctx.set_local(name, res)
                return

            ctx.set_nonlocal(name, res)

        else:

            ref = ctx.local if to_new_ctx else ctx.get_nonlocal_env(name)

            *fst_n, [last] = trailers
            for each, in fst_n:
                if each.name == 'symbol':
                    ref = getattr(ref, each[0])
                else:
                    item = tuple(ast_for_expr_cons(each[0], ctx))
                    if len(item) == 1:
                        item = item[0]
                    ref = ref[item]

            if last.name == 'symbol':
                setattr(ref, last[0], res)
            else:
                item = tuple(ast_for_expr_cons(last[0], ctx))
                if len(item) == 1:
                    item = item
                ref[item] = res

        return

    elif sexpr.name == 'label':
        [[label]] = sexpr
        ctx.set_local('@label', label)

    elif sexpr.name == 'into':
        [[label]] = sexpr
        return BreakUntil(label)

    elif sexpr.name == 'importExpr':
        if sexpr[0].name != 'remImport':
            exec(''.join(flatten(sexpr[0])).replace('`', ' ').strip(), ctx.local)
            return

        import os
        [path], *name = sexpr[0]
        path = eval(path)

        manager = ctx.module_manager

        if not name:
            name = os.path.split(os.path.splitext(path)[0])[1]
        else:
            [[name]] = name

        if path in manager['@modules']:
            return

        manager['@modules'].add(path)

        with open(path, 'r') as src_file:
            src = src_file.read()

        env = ReferenceDict(
            default.default,
            module_manager=manager)

        env.update(
            __name__=name,
            __token__=ctx['__token'],
            eval=lambda src: ast_for_file(rem_parser(env['__token__'](src),
                                                     meta=MetaInfo(),
                                                     partial=False), env))
        env['@module_manager'] = manager
        env['中文编程'] = lambda: env['__token__'].mut_by(env['cast'](env['to_chinese']))
        manager[name] = env

        rem_eval(rem_parser(env['__token__'](src),
                            meta=MetaInfo(fileName=path),
                            partial=False),
                 env)

    else:
        raise TypeError('unknown statement.')


def ast_for_inv_exp(inv: Ast, ctx: ReferenceDict):
    atom_expr, *inv_trailers = inv
    res = ast_for_atom_expr(atom_expr, ctx)

    if isinstance(res, BreakUntil) and ctx.get_local('@label') != res:
        return res

    for each in inv_trailers:
        if each.name == 'atomExpr':
            arg = ast_for_atom_expr(each, ctx)
            if isinstance(arg, BreakUntil) and ctx.get_local('@label') != arg:
                return arg

            res = res(arg)

        else:  # invTrailer
            arg = ast_for_atom_expr(each[0], ctx)
            if isinstance(arg, BreakUntil) and ctx.get_local('@label') != arg:
                return arg

            res = arg(res)

    return res


def ast_for_expr(expr: Ast, ctx: ReferenceDict):
    if expr[-1].name == 'where':
        head, *then_trailers, where = expr
        stmts = where[0]
        res = ast_for_statements(stmts, ctx)
        if isinstance(res, BreakUntil) and ctx.get_local('@label') != res:
            return res

    else:
        head, *then_trailers = expr

    res = ast_for_test_expr(head, ctx)

    if isinstance(res, BreakUntil) and ctx.get_local('@label') != res:
        return res

    for each in then_trailers:

        arg = ast_for_test_expr(each[0], ctx)

        if isinstance(arg, BreakUntil) and ctx.get_local('@label') != arg:
            return arg

        res = arg(res) if each.name == 'thenTrailer' else res(arg)

    return res


def ast_for_as_expr(as_expr: Ast, ctx: ReferenceDict, test_exp):
    many = None
    when = None
    statements = None

    for each in as_expr:
        if each.name == 'argMany':
            many = each
        elif each.name == 'expr':
            when = each
        elif each.name == 'statements':
            statements = each

    new_ctx = ctx.branch()
    if many and not pattern_match(many, test_exp, new_ctx):
        return None
    if when and not ast_for_expr(when, new_ctx):
        return None

    ctx.update(new_ctx.local)
    if not statements:
        return None

    else:
        return ast_for_statements(statements, ctx)


def ast_for_case_expr(case_expr: Ast, ctx: ReferenceDict):
    test, *cases = case_expr
    right = ast_for_expr(test, ctx)

    if isinstance(right, BreakUntil) and ctx.get_local('@label') != right:
        return right

    for case in cases:
        res = ast_for_as_expr(case, ctx, right)
        if res:
            return res


def ast_for_test_expr(test: Ast, ctx: ReferenceDict):
    sexpr = test[0]
    if sexpr.name == 'caseExp':
        res = ast_for_case_expr(sexpr, ctx)
    elif sexpr.name == 'binExp':
        res = ast_for_bin_expr(sexpr, ctx)
    else:
        raise TypeError('unknown test expr.')

    return res


def parse_bin_exp(left, mid, right, ctx: ReferenceDict):
    if isinstance(left, BinExp):
        left = parse_bin_exp(*left, ctx)
    else:
        left = ast_for_factor(left, ctx)

    if isinstance(left, BreakUntil) and ctx.get_local('@label') != left:
        return left

    if isinstance(right, BinExp):
        right = parse_bin_exp(*right, ctx)
    else:
        right = ast_for_factor(right, ctx)

    if isinstance(right, BreakUntil) and ctx.get_local('@label') != right:
        return right

    res = bin_op_fns[mid](left, right)
    return res


def ast_for_bin_expr(bin_expr: Ast, ctx: ReferenceDict):
    if len(bin_expr) is not 1:
        bin_expr = order_dual_opt(bin_expr)
        left, mid, right = bin_expr
        return parse_bin_exp(left, mid, right, ctx)

    else:
        [factor] = bin_expr
        return ast_for_factor(factor, ctx)


def ast_for_factor(factor: Ast, ctx: ReferenceDict):
    unary_op = None
    if factor[0].name == 'unaryOp':
        unary_op, inv, *suffix = factor
    else:
        inv, *suffix = factor

    res = ast_for_inv_exp(inv, ctx)

    if isinstance(res, BreakUntil) and ctx.get_local('@label') != res:
        return res

    if suffix:

        [[suffix]] = suffix

        if suffix is '?':

            res = True if res else False

        else:

            res = res is None

    if unary_op:
        [unary_op] = unary_op
        if unary_op is '+':
            return res
        elif unary_op is '-':
            return -res
        else:  # not
            return not res

    return res


def ast_for_atom_expr(atom_expr: Ast, ctx: ReferenceDict):
    atom, *trailers = atom_expr
    res = ast_for_atom(atom, ctx)
    if isinstance(res, BreakUntil) and ctx.get_local('@label') != res:
        return res

    for each, in trailers:
        if each.name == 'symbol':
            name = each[0]
            res = getattr(res, name)

        else:
            item = tuple(ast_for_expr_cons(each, ctx))
            if len(item) is 1:
                item = item[0]

            if isinstance(item, BreakUntil) and ctx.get_local('@label') != item:
                return item

            res = res[item]
    return res


def ast_for_atom(atom: Ast, ctx: ReferenceDict):
    if len(atom) is 1:
        sexpr = atom[0]
        if sexpr.name == 'refName':
            *ref, (name,) = sexpr
            if ref:
                return RefName(name)

            ctx = ctx.get_nonlocal_env(name)

            return ctx[name]

        elif sexpr.name == 'const':
            if sexpr[0][1] == 'T':
                return True
            elif sexpr[0][1] == 'F':
                return False
            else:
                return None

        elif sexpr.name == 'number':
            return eval(sexpr[0])

        elif sexpr.name == 'lambdef':
            return ast_for_lambdef(sexpr, ctx)

        elif sexpr.name == 'listCons':
            if not sexpr:
                return list()
            return list(ast_for_expr_cons(sexpr[0], ctx))

        elif sexpr.name == 'tupleCons':
            if not sexpr:
                return tuple()
            return tuple(ast_for_expr_cons(sexpr[0], ctx))

        elif sexpr.name == 'setCons':
            if not sexpr:
                return set()
            return set(ast_for_expr_cons(sexpr[0], ctx))

        elif sexpr.name == 'dictCons':
            if not sexpr:
                return dict()
            return dict(ast_for_kv_cons(sexpr[0], ctx))

        elif sexpr.name == 'compreh':
            return ast_for_comprehension(sexpr, ctx)
        elif sexpr.name == 'string':
            return eval(sexpr[0])

    elif atom[0] is '(':
        return ast_for_expr(atom[1], ctx)
    else:
        return eval(''.join(each[0] for each in atom))


def ast_for_expr_cons(expr_cons: Ast, ctx: ReferenceDict):
    for each in expr_cons:
        if each.name == 'unpack':
            yield from ast_for_expr(each[0], ctx)
        else:
            for e in each:
                e = ast_for_expr(e, ctx)
                yield e


def ast_for_kv_cons(expr_cons: Ast, ctx: ReferenceDict):
    for each in expr_cons:
        if each.name == 'unpack':
            iterator = ast_for_expr(each[0], ctx)
            yield from iterator.items() if isinstance(iterator, dict) else iterator

        else:
            for k, v in each:
                yield ast_for_expr(k, ctx), ast_for_expr(v, ctx)


def _scp(f, xs):
    for e in xs:
        f = f(e)
    return f


def ast_for_comprehension(comprehension: Ast, ctx: ReferenceDict):
    ctx = ctx.branch()

    if comprehension[1] == '`not`':
        collections, _, lambdef = comprehension
        is_yield = False
    else:
        collections, lambdef = comprehension
        is_yield = True

    collections = [ast_for_expr(each, ctx) for each in collections]
    lambdef = ast_for_lambdef(lambdef, ctx)

    if is_yield:
        return (_scp(lambdef, each) for each in itertools.product(*collections))

    e = None
    for each in itertools.product(*collections):
        e = _scp(lambdef, each)
        if isinstance(e, BreakUntil) and ctx.get_local('@label') != e:
            return e
    return e


def ast_for_lambdef(lambdef: Ast, ctx: ReferenceDict):
    if len(lambdef) is 1:
        if lambdef[0].name == 'singleArgs':
            return Fn(list(each[0] for each in lambdef[0]), {}, (ctx, None))
        else:
            return Fn((), {}, (ctx, lambdef[0]))

    elif len(lambdef) is 2:
        args, stmts = lambdef
        args = list(each[0] for each in args)
        return Fn(args, {}, (ctx, stmts))

    else:
        return lambda: None


class Fn:
    __slots__ = ['uneval_args', 'eval_args', 'body']

    def __init__(self, uneval, eval, body):
        self.uneval_args = uneval
        self.eval_args = eval
        self.body = body

    def __call__(self, arg=()):

        if not self.uneval_args and not arg:
            ctx, stmts = self.body
            new_ctx: 'ReferenceDict' = ctx.branch()
            new_ctx.update(self.eval_args)
            return ast_for_statements(stmts, new_ctx)

        eval_args = self.eval_args.copy()
        eval_args[self.uneval_args[0]] = arg
        uneval_args = self.uneval_args[1:]

        if not uneval_args:
            ctx, stmts = self.body
            new_ctx: 'ReferenceDict' = ctx.branch()
            new_ctx.update(eval_args)
            return ast_for_statements(stmts, new_ctx)
        return Fn(uneval_args, eval_args, self.body)

    @staticmethod
    def apply_many(self, *args):
        eval_args = self.eval_args.copy()
        eval_args = eval_args.update(dict(zip(self.uneval_args, *args)))
        uneval_args = self.uneval_args[len(args):]
        if not uneval_args:
            ctx, stmts = self.body
            new_ctx = ctx.branch()
            new_ctx.update(eval_args)
            return ast_for_statements(stmts, new_ctx)
        return Fn(uneval_args, eval_args, self.body)


def _pattern_match(left_e, right_e, ctx):
    try:
        if left_e is '_':
            right_e.clear()
            return True

        elif left_e.name == 'refName':
            [*ref, (name,)] = left_e

            if ref:
                return ctx.get_nonlocal(name) == right_e
            else:
                ctx.set_local(name, right_e)
                return True

        elif left_e.name == 'string':
            return eval(left_e[0]) == right_e

        elif left_e.name == 'const':
            const = left_e[0]
            return {'`True`': True,
                    '`False`': False,
                    '`None`': None}[const] is right_e


        elif left_e.name == 'number':
            return eval(left_e[0]) == right_e

        elif left_e.name == 'tupleArg':
            many = left_e[0]
            return pattern_match(many, right_e, ctx)

        else:
            assert False

    except:
        return False


def pattern_match(left, right, ctx):
    try:
        is_iter: bool = False
        if left[-1].name == 'iterMark':
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
                if k[0] == '...':
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


def ast_for_file(file_source_parsed: Ast, ctx):
    if file_source_parsed:
        return ast_for_statements(file_source_parsed[0], ctx)


def rem_eval(ast: Ast, env: ReferenceDict):
    ast_for_file(ast, env)
    return env
