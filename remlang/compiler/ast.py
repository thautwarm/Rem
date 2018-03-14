from Ruikowa.ObjectRegex.ASTDef import Ast
from typing import Optional, Tuple
from .order_dual_opt import order_dual_opt, BinExp, bin_op_fns, op_priority
import itertools
from functools import reduce


class RefName:
    def __init__(self, name):
        self.name = name


class BreakUntil:
    __slots__ = ['name']

    def __init__(self, name):
        self.name = name


def ast_for_statements(statements: Ast, ctx: dict) -> Optional:
    res = None
    for each in statements:
        res = ast_for_statement(each, ctx)
        if isinstance(res, BreakUntil) and ctx.get('@label') != res:
            return res
    return res


def ast_for_statement(statement: Ast, ctx: dict) -> Optional:
    sexpr = statement[0]

    if sexpr.name == 'expr':
        if len(statement) is 2:
            res = ast_for_expr(sexpr, ctx)
            if isinstance(res, BreakUntil) and ctx.get('@label') != res:
                return res

        else:
            res = ast_for_expr(sexpr, ctx)
            if isinstance(res, BreakUntil) and ctx.get('@label') != res:
                return res
            return res

    elif sexpr.name == 'let':
        (name,), expr = sexpr
        res = ast_for_expr(expr, ctx)
        if isinstance(res, BreakUntil) and ctx.get('@label') != res:
            return res
        ctx[name] = res
        return None

    elif sexpr.name == 'label':
        [[label]] = sexpr
        ctx['@label'] = label

    elif sexpr.name == 'breakUntil':
        [[label]] = sexpr
        return BreakUntil(label)

    else:
        raise TypeError('unknown statement.')


def ast_for_inv_exp(inv: Ast, ctx: dict):
    atom_expr, *inv_trailers = inv
    res = ast_for_atom_expr(atom_expr, ctx)

    if isinstance(res, BreakUntil) and ctx.get('@label') != res:
        return res

    for each in inv_trailers:

        arg = ast_for_atom_expr(each[0], ctx)

        if isinstance(arg, BreakUntil) and ctx.get('@label') != arg:
            return arg

        res = arg(res)

    return res


def ast_for_expr(expr: Ast, ctx: dict):
    if expr[-1].name == 'where':
        call, *then_trailers, where = expr
        stmts = where[0]
        res = ast_for_statements(stmts, ctx)
        if isinstance(res, BreakUntil) and ctx.get('@label') != res:
            return res

    else:
        call, *then_trailers = expr

    res = ast_for_call_expr(call, ctx)

    if isinstance(res, BreakUntil) and ctx.get('@label') != res:
        return res

    for each in then_trailers:
        arg = ast_for_call_expr(each[0], ctx)

        if isinstance(arg, BreakUntil) and ctx.get('@label') != arg:
            return arg

        res = arg(res)

    return res


def ast_for_call_expr(call: Ast, ctx: dict):
    head, *tail = call
    res = ast_for_test_expr(head, ctx)

    if isinstance(res, BreakUntil) and ctx.get('@label') != res:
        return res

    for each in tail:
        arg = ast_for_test_expr(each, ctx)
        if isinstance(arg, BreakUntil) and ctx.get('@label') != arg:
            return arg
        res = res(arg)
    return res


def ast_for_as_expr(as_expr: Ast, ctx, test_exp):
    when = None
    statements = None
    if len(as_expr) is 4:
        many, _, when, statements = as_expr
    elif len(as_expr) is 3:
        many, _, when = as_expr

    elif len(as_expr) is 2:
        many, statements = as_expr

    else:
        many, = as_expr

    new_ctx = ctx.copy()
    if not pattern_match(many, test_exp, ctx, new_ctx):
        return None
    if when and not ast_for_expr(when, new_ctx):
        return None
    if not statements:
        return None

    else:
        return ast_for_statements(statements, new_ctx)


def ast_for_case_expr(case_expr: Ast, ctx):
    test, *cases = case_expr
    right = ast_for_expr(test, ctx)

    for case in cases:
        res = ast_for_as_expr(case, ctx, right)
        if res:
            return res


def ast_for_test_expr(test: Ast, ctx: dict):
    sexpr = test[0]
    # print(sexpr)
    if sexpr.name == 'caseExp':
        res = ast_for_case_expr(sexpr, ctx)
    elif sexpr.name == 'binExp':
        res = ast_for_bin_expr(sexpr, ctx)
    else:
        raise TypeError('unknown test expr.')

    return res


def parse_bin_exp(left, mid, right, ctx: dict):
    if isinstance(left, BinExp):
        left = parse_bin_exp(*left, ctx)
    else:
        left = ast_for_factor(left, ctx)

    if isinstance(left, BreakUntil) and ctx.get('@label') != left:
        return left

    if isinstance(right, BinExp):
        right = parse_bin_exp(*right, ctx)
    else:
        right = ast_for_factor(right, ctx)

    if isinstance(right, BreakUntil) and ctx.get('@label') != right:
        return right

    res = bin_op_fns[mid](left, right)
    return res


def ast_for_bin_expr(bin: Ast, ctx: dict):
    if len(bin) is not 1:
        bin = order_dual_opt(bin)
        left, mid, right = bin
        return parse_bin_exp(left, mid, right, ctx)

    else:
        [factor] = bin
        return ast_for_factor(factor, ctx)


def ast_for_factor(factor: Ast, ctx: dict):
    unary_op = None
    if factor[0].name == 'unaryOp':
        unary_op, inv, *suffix = factor
    else:
        inv, *suffix = factor

    res = ast_for_inv_exp(inv, ctx)

    if isinstance(res, BreakUntil) and ctx.get('@label') != res:
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

    return res


def ast_for_atom_expr(atom_expr: Ast, ctx: dict):
    atom, *trailers = atom_expr
    res = ast_for_atom(atom, ctx)
    if isinstance(res, BreakUntil) and ctx.get('@label') != res:
        return res

    for each in trailers:
        [expr_cons] = each

        item = tuple(ast_for_expr_cons(expr_cons, ctx))
        if len(item) is 1:
            item = item[0]

        if isinstance(item, BreakUntil) and ctx.get('@label') != item:
            return item

        res = res[item]
    return res


def ast_for_atom(atom: Ast, ctx: dict):
    if len(atom) is 1:
        sexpr = atom[0]
        if sexpr.name == 'refName':
            *ref, (name,) = sexpr
            if ref:
                return RefName(name)

            while ctx and name not in ctx:
                try:
                    ctx = ctx["@parent"]
                except KeyError:
                    raise NameError(name)

            if ctx and name in ctx:
                res = ctx.get(name)
                return res

            raise NameError(name)

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
            return sexpr[0]

    elif isinstance(atom[0], Ast):
        return ''.join(each[0] for each in atom)
    else:
        return ast_for_expr(atom[1], ctx)


def ast_for_expr_cons(expr_cons: Ast, ctx: dict):
    for each in expr_cons:
        if each.name == 'unpack':
            yield from ast_for_expr(each[0], ctx)
        else:
            for e in each:
                e = ast_for_expr(e, ctx)
                yield e


def ast_for_kv_cons(expr_cons: Ast, ctx: dict):
    if not expr_cons:
        return ()

    for each in expr_cons:
        if each.name == 'unpack':
            iterator = ast_for_expr(each[0], ctx)
            yield from iterator.items() if isinstance(iterator, dict) else iterator

        else:
            for k, v in each:
                yield ast_for_expr(k, ctx), ast_for_expr(v, ctx)


def ast_for_comprehension(comprehension: Ast, ctx):
    new_ctx = ctx.copy()
    new_ctx['@parent'] = ctx
    ctx = new_ctx

    collections, lambdef = comprehension
    collections = [ast_for_expr(each, ctx) for each in collections]
    lambdef = ast_for_lambdef(lambdef, ctx)
    return (reduce(lambda a, b: a(b), each, lambdef) for each in itertools.product(*collections))


def ast_for_lambdef(lambdef: Ast, ctx: dict):
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
        return lambda x: None


class Fn:
    __slots__ = ['uneval_args', 'eval_args', 'body']

    def __init__(self, uneval, eval, body: Tuple[dict, Optional[Ast]]):
        self.uneval_args = uneval
        self.eval_args = eval
        self.body = body

    def __call__(self, arg=()):

        if not self.uneval_args and not arg:
            ctx, stmts = self.body
            new_ctx = ctx.copy()
            new_ctx['@parent'] = ctx
            new_ctx.update(self.eval_args)
            return ast_for_statements(stmts, new_ctx)

        eval_args = self.eval_args.copy()
        eval_args[self.uneval_args[0]] = arg
        uneval_args = self.uneval_args[1:]

        if not uneval_args:
            ctx, stmts = self.body
            new_ctx = ctx.copy()
            new_ctx['@parent'] = ctx
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
            ctx = ctx.copy()
            return ast_for_statements(stmts, ctx)
        return Fn(uneval_args, eval_args, self.body)


def _pattern_match(left_e, right_e, ctx, new_ctx):
    arg = left_e[0]

    try:
        if arg is '_':
            return True

        elif arg.name == 'refName':
            [*ref, (name,)] = arg

            if ref:
                return ctx[name] == right_e
            else:

                new_ctx[name] = right_e

                return True

        elif arg.name == 'string':
            left_e = ''.join(each[0] for each in left_e)
            if left_e != right_e:
                raise Exception
        elif arg.name == 'const':
            const = arg[0]
            return {'`True`': True,
                    '`False`': False,
                    '`None`': None}[const] is right_e


        elif arg.name == 'number':
            return eval(arg[0]) == right_e

        elif arg.name == 'tupleArg':
            many = arg[0]

            return pattern_match(many, right_e, ctx, new_ctx)

        else:
            assert False
    except:
        return False

    return True


def pattern_match(left, right, ctx, new_ctx):
    try:
        is_iter: bool = False
        if left[-1].name == 'iterMark':
            left.pop()
            is_iter = True
        elif len(left) > 1:
            is_iter = True

        if not is_iter:
            return _pattern_match(left[0], right, ctx, new_ctx)
        left = iter(left)
        right = iter(right)

        while True:
            try:
                k = next(left)
            except StopIteration:
                return True

            if k[0] == '...':
                k = k[1:]
                return _pattern_match(k, tuple(right), ctx, new_ctx)
            else:
                v = next(right)
                if not _pattern_match(k, v, ctx, new_ctx):
                    return False

    except Exception as e:
        print(e)
        return False


def ast_for_file(file: Ast, ctx):
    if file:
        return ast_for_statements(file[0], ctx)
