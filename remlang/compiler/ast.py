import itertools
from Ruikowa.ObjectRegex.ASTDef import Ast
from Ruikowa.ErrorFamily import handle_error
from Ruikowa.ObjectRegex.MetaInfo import MetaInfo
from .reference_collections import ReferenceDict
from .order_dual_opt import order_dual_opt, BinExp, bin_op_fns
from .rem_parser import file
from .utils import flatten
from .module import default_env, make_new_module, md5
from .pattern_matching import pattern_match, unmatched
from .control_flow import BreakUntil
from .err import Trace

rem_parser = handle_error(file)


# default settings. eval
def add_eval_func(to: 'ReferenceDict'):
    to['eval'] = lambda src: ast_for_file(
        rem_parser(
            to['__token__'](src),
            meta=MetaInfo(fileName='<eval input>'),
            partial=False),
        to)


# this is the main module
main = make_new_module('main', default_env)
add_eval_func(to=main)


class RefName:
    def __init__(self, name):
        self.name = name


def ast_for_statements(statements: Ast, ctx: ReferenceDict):
    """
    statements Throw [T]
        ::= statement ([T] statement)*;
    """
    res = None
    for each in statements:
        try:
            res = ast_for_statement(each, ctx)
        except BreakUntil as e:
            if e.name != ctx.get_local('@label'):
                raise e
    return res


def ast_for_statement(statement: Ast, ctx: ReferenceDict):
    """
    statement
        ::= (label | let | expr | into | importExpr) [';'];
    """
    # assert statement.name == 'statement'
    sexpr = statement[0]
    s_name: str = sexpr.name
    try:
        if s_name[0] is 'e':  # expr
            # RuikoEBNF:
            # expr ::=  testExpr (thenTrailer | applicationTrailer)* [where];
            if len(statement) is 2:
                # end with ';' then return None
                ast_for_expr(sexpr, ctx)
            else:
                res = ast_for_expr(sexpr, ctx)
                return res

        elif s_name[0] is 'l':
            if s_name[1] is 'a':  # label
                [[label]] = sexpr
                ctx.set_local('@label', label)
                return
            # else: let

            # RuikoEBNF:
            # let  Throw ['=' '!']
            #   ::= ['`let`'] symbol ['!' trailer+] '=' expr;

            to_new_ctx = False

            if isinstance(sexpr[0], str):
                # bind a new var in current environment(closure).
                to_new_ctx = True
                sexpr = sexpr[1:]

            # For the readability of source codes,
            #   pattern matching using list destruction is better.
            [name], *trailers, expr = sexpr

            res = ast_for_expr(expr, ctx)

            if not trailers:
                # let symbol = ...

                if to_new_ctx or name in ctx:
                    ctx.set_local(name, res)
                    return

                ctx.set_nonlocal(name, res)

            else:
                # let symbol !.attr = ... | let symbol ![item] = ...

                ref = ctx.local if to_new_ctx else ctx.get_nonlocal_env(name)

                *fst_n, [last] = trailers

                # `trailers` is a list of trailer.
                # RuikoEBNF:
                # trailer Throw ['[' ']' '.']
                #   ::= '[' exprCons ']' | '.' symbol;

                for each, in fst_n:
                    if each.name[0] is 's':  # symbol
                        ref = getattr(ref, each[0])
                    else:  # [exprCons]
                        item = tuple(ast_for_expr_cons(each[0], ctx))
                        if len(item) == 1:
                            item = item[0]
                        ref = ref[item]

                if last.name[0] == 's':  # symbol
                    # trailer = . symbol
                    setattr(ref, last[0], res)
                else:
                    # trailer = [exprCons]
                    item = tuple(ast_for_expr_cons(last[0], ctx))
                    if len(item) == 1:
                        item = item
                    ref[item] = res

            # let expr return None

        elif s_name[0] is 'i':

            if s_name[1] is 'n':  # into
                # RuikoEBNF:
                # into Throw ['`into`']
                #       ::= '`into`' symbol;
                [[label]] = sexpr
                # TODO with result
                raise BreakUntil(label)
            # else: importExpr

            # RuikoEBNF:
            # importExpr
            #   ::= singleImportExpr | fromImportExpr | remImport;

            if sexpr[0].name[0] is not 'r':
                # singleImportExpr | fromImportExpr
                exec(''.join(flatten(sexpr[0])).replace('`', ' ').strip(), ctx.local)
                return

            import os
            [path], *name = sexpr[0]
            path = eval(path)

            manager = ctx.module_manager

            if not name:
                # get the filename without ext
                name = os.path.split(os.path.splitext(path)[0])[1]
            else:
                [[name]] = name

            src, md5_v = md5(path)

            managed_modules = manager['@modules']
            if md5_v == managed_modules.get(path):
                # imported and file not changed.
                # so do not import again
                return

            # or update new md5 value
            managed_modules[path] = md5_v

            env = make_new_module(name,
                                  module_manager=manager,
                                  token_manager=ctx['__token__'])
            add_eval_func(to=env)

            rem_eval(rem_parser(env['__token__'](src),
                                meta=MetaInfo(fileName=path),
                                partial=False),
                     env)

        else:
            raise TypeError('unknown statement.')
    except BreakUntil as e:
        raise e
    except Exception as e:
        print(statement.meta)
        raise Trace(e, statement.meta)


def ast_for_expr(expr: 'Ast', ctx: ReferenceDict):
    """
    expr
        ::=  testExpr (thenTrailer | applicationTrailer)*
            [where];
    """
    # assert expr.name == 'expr'
    if expr[-1].name[0] is 'w':  # where
        # if expr[-1].name == 'where':
        head, *then_trailers, where = expr
        stmts = where[0]
        res = ast_for_statements(stmts, ctx)

    else:
        head, *then_trailers = expr

    res = ast_for_test_expr(head, ctx)

    for each in then_trailers:
        arg = ast_for_test_expr(each[0], ctx)

        res = arg(res) if each.name[0] is 't' else res(arg)
        # res = arg(res) if each.name == 'thenTrailer' else res(arg)

    return res


def ast_for_test_expr(test: Ast, ctx: ReferenceDict):
    """
    testExpr ::= caseExp | binExp;
    """
    # assert test.name == 'testExpr'
    sexpr = test[0]
    if sexpr.name[0] is 'c':
        # if sexpr.name == 'caseExp':
        res = ast_for_case_expr(sexpr, ctx)

    else:
        # elif sexpr.name == 'binExp':
        res = ast_for_bin_expr(sexpr, ctx)

    return res


def ast_for_case_expr(case_expr: 'Ast', ctx: 'ReferenceDict'):
    """
    caseExp Throw ['`case`', '`end`', T]
        ::= '`case`' expr [T] asExp* [otherwiseExp] [T] '`end`';
    """
    # assert case_expr.name == 'caseExp'

    test, *cases = case_expr
    right = ast_for_expr(test, ctx)

    for case in cases:
        res = ast_for_as_expr(case, ctx, right)

        # do not use None to represent the matching status
        #   just think `case None as x => x end` should match.
        if res is not unmatched:
            return res


def ast_for_as_expr(as_expr: 'Ast', ctx: 'ReferenceDict', test_exp: 'BinExp'):
    """
    asExp  Throw ['=>', T, '`as`', '`when`']
        ::= ['`as`' argMany]
            [
              [T] '`when`' [T] expr
            ]
            [T]
            ['=>' [T] [statements]];
    """
    # assert as_expr.name == 'asExp'

    many = None
    when = None
    statements = None

    for each in as_expr:

        if each.name[0] is 'a':
            # if each.name == 'argMany':
            many = each
        elif each.name[0] is 'e':
            # elif each.name == 'expr':
            when = each
        elif each.name[0] == 's':
            # elif each.name == 'statements':
            statements = each

    try:
        new_ctx = ctx.branch()
        if many and not pattern_match(many, test_exp, new_ctx):
            return unmatched
        if when and not ast_for_expr(when, new_ctx):
            return unmatched

        ctx.update(new_ctx.local)
        if not statements:
            return unmatched

        return ast_for_statements(statements, ctx)

    except BreakUntil as e:
        if e.name != ctx.get_local('@label'):
            raise e


def ast_for_bin_expr(bin_expr: 'Ast', ctx: 'ReferenceDict'):
    """
    binExp ::= factor (
        ('+'    | '-'   | '*'   | '/' | '%'  |
         '++'   | '--'  | '**'  | '//'|
         '^'    | '&'   | '|'   | '>>'| '<<' |
         '^^'   | '&&'  | '||'  |
         '`and`'| '`or`'| '`in`'| '`is`'     |
         '|>'   |
         '>'    | '<'   | '>='  | '<='|
         '=='   | '!='  |
         '<-')
        factor)*;
    """
    # assert bin_expr.name == 'binExp'

    if len(bin_expr) is not 1:
        bin_expr = order_dual_opt(bin_expr)
        left, mid, right = bin_expr
        return parse_bin_exp(left, mid, right, ctx)

    else:
        [factor] = bin_expr
        return ast_for_factor(factor, ctx)


def parse_bin_exp(left, mid, right, ctx: 'ReferenceDict'):
    if isinstance(left, BinExp):
        left = parse_bin_exp(*left, ctx)
    else:
        left = ast_for_factor(left, ctx)

    if isinstance(right, BinExp):
        right = parse_bin_exp(*right, ctx)
    else:
        right = ast_for_factor(right, ctx)

    res = bin_op_fns[mid](left, right)
    return res


def ast_for_factor(factor: 'Ast', ctx: 'ReferenceDict'):
    """
    factor ::= [unaryOp] invExp [suffix];
    """
    # assert factor.name == 'factor'
    unary_op = None
    suffix = None
    if factor[0].name[0] is 'u':
        # if factor[0].name == 'unaryOp':
        if factor[-1].name[0] is 's':
            # if factor[-1].name == 'suffix':
            [unary_op], inv, [suffix] = factor
        else:
            [unary_op], inv = factor
    elif factor[-1].name[0] == 's':
        # elif factor[-1].name == 'suffix':
        inv, [suffix] = factor
    else:
        inv, = factor

    res = ast_for_inv_exp(inv, ctx)

    if suffix:
        if suffix is '?':
            res = True if res else False
        else:
            # '??'
            res = res is not None

    if unary_op:
        if unary_op is '+':
            return res
        elif unary_op is '-':
            return -res
        else:  # not
            return not res

    return res


def ast_for_inv_exp(inv: 'Ast', ctx: 'ReferenceDict'):
    """
    invExp  ::= atomExpr (atomExpr | invTrailer)*;
    """
    # assert inv.name == 'invExp'
    atom_expr, *inv_trailers = inv
    res = ast_for_atom_expr(atom_expr, ctx)

    for each in inv_trailers:
        if each.name[0] is 'a':
            # if each.name == 'atomExpr':
            # RuikoEBNF
            # atomExpr Throw['!', T]
            #   ::= atom ['!' ([T] trailer)+];
            arg = ast_for_atom_expr(each, ctx)

            res = res(arg)

        else:  # invTrailer
            # RuikoEBNF:
            # invTrailer Throw ['.'] ::= '.' atomExpr;
            arg = ast_for_atom_expr(each[0], ctx)

            res = arg(res)

    return res


def ast_for_atom_expr(atom_expr: 'Ast', ctx: 'ReferenceDict'):
    """
    atomExpr Throw[T] ::= atom ([T] trailer)*;
    """
    # assert atom_expr.name == 'atomExpr'
    atom, *trailers = atom_expr
    res = ast_for_atom(atom, ctx)
    try:
        for each, in trailers:
            # RuikoEBNF
            # trailer Throw ['!' '[' ']' '\'']
            #       ::= '!' '[' exprCons ']' | '\'' symbol;
            if each.name[0] is 's':
                # if each.name == 'symbol':
                name = each[0]
                res = getattr(res, name)

            else:
                # elif each.name == 'exprCons':
                item = tuple(ast_for_expr_cons(each, ctx))
                if len(item) is 1:
                    item = item[0]

                res = res[item]

        return res
    except BreakUntil as e:
        raise e
    except Exception as e:
        raise Trace(e, atom_expr.meta)


def ast_for_atom(atom: 'Ast', ctx: 'ReferenceDict'):
    """
    atom  Throw ['++']
        ::=  refName | const | string ('++' string)* | number |
            '(' expr ')'|
             listCons | tupleCons | setCons | dictCons | compreh |
             lambdef;
    """
    # assert atom.name == 'atom'
    if len(atom) is 1:
        sexpr = atom[0]
        s_name = sexpr.name
        if s_name[0] is 'r':
            # if s_name == 'refName':

            *ref, [name] = sexpr
            if ref:
                return RefName(name)

            ctx = ctx.get_nonlocal_env(name)
            return ctx[name]

        elif s_name[0] is 'c':
            if s_name[2] is 'n':  # const
                # const ::=  R'`True`|`False`|`None`';
                if sexpr[0][1] is 'T':
                    return True
                elif sexpr[0][1] is 'F':
                    return False
                else:  # None
                    return None

            # comprehension

            try:
                return ast_for_comprehension(sexpr, ctx)
            except BreakUntil as e:
                if e.name != ctx.get_local('@label'):
                    raise e

        elif s_name[0] is 'n':
            # elif s_name == 'number':
            return eval(sexpr[0])

        elif s_name[0] is 'l':
            if s_name[1] is 'a':  # lambdef
                return ast_for_lambdef(sexpr, ctx)
            # listCons
            if not sexpr:
                return list()
            return list(ast_for_expr_cons(sexpr[0], ctx))

        elif s_name[0] is 't':  # tupleCons
            if not sexpr:
                return tuple()
            return tuple(ast_for_expr_cons(sexpr[0], ctx))

        elif s_name[0] is 's':
            if s_name[1] is 't':  # string
                return eval(sexpr[0])

            # setCons
            if not sexpr:
                return set()
            return set(ast_for_expr_cons(sexpr[0], ctx))

        elif s_name[0] is 'd':  # dictCons
            if not sexpr:
                return dict()
            return dict(ast_for_kv_cons(sexpr[0], ctx))

    elif atom[0] is '(':  # '(' expr ')'
        return ast_for_expr(atom[1], ctx)
    else:  # string ('++' string)*
        return ''.join(eval(each[0]) for each in atom)


def ast_for_expr_cons(expr_cons: 'Ast', ctx: 'ReferenceDict'):
    """
    exprCons Throw [',' T] ::= exprMany ([T] ',' [T] unpack [[T] ',' [T] exprMany])* [','];
    """
    for each in expr_cons:
        if each.name[0] is 'u':  # unpack
            yield from ast_for_expr(each[0], ctx)
        else:
            for e in each:
                e = ast_for_expr(e, ctx)
                yield e


def ast_for_kv_cons(expr_cons: Ast, ctx: ReferenceDict):
    """
    kvCons   Throw [',' T]    ::= kvMany ([T] ',' [T] unpack [[T] ',' [T] kvMany])* [','];
    """
    for each in expr_cons:
        if each.name[0] is 'u':  # unpack
            iterator = ast_for_expr(each[0], ctx)
            yield from iterator.items() if isinstance(iterator, dict) else iterator

        else:
            for k, v in each:
                yield ast_for_expr(k, ctx), ast_for_expr(v, ctx)


def _scp(f, xs):
    for e in xs:
        f = f(e)
    return f


def ast_for_comprehension(comprehension: 'Ast', ctx: 'ReferenceDict'):
    """
    compreh  Throw['`from`' '`yield`' T]
        ::=  '`from`' [T] exprMany [[T] '`not`'] [T] '`yield`' [T] lambdef;
    """
    # assert comprehension.name == 'compreh'

    new_ctx = ctx.branch()
    if comprehension[1] == '`not`':
        collections, _, lambdef = comprehension
        is_yield = False
    else:
        collections, lambdef = comprehension
        is_yield = True

    try:
        cartesian_prod_collections = itertools.product(
            *(ast_for_expr(each, new_ctx) for each in collections))

        lambdef = ast_for_lambdef(lambdef, new_ctx)

        if is_yield:
            return (_scp(lambdef, each) for each in cartesian_prod_collections)

        e = None
        for each in cartesian_prod_collections:
            e = _scp(lambdef, each)

        return e

    except BreakUntil as e:
        if e.name != ctx.get_local('@label'):
            raise e


def ast_for_lambdef(lambdef: 'Ast', ctx: 'ReferenceDict'):
    """
    lambdef Throw ['{', '}', '|', ',', '`from`', '`let`', '`end`', T]
        ::= '{' [T]
                ['|' [singleArgs [T]] '|']
                [T]
                [statements [T]]
            '}'
            |
            '`from`' [T]
                [singleArgs [T]]
            '`let`' [T]
                [statements [T]]
            '`end`'
            ;
    """
    # assert lambdef.name == 'lambdef'
    if len(lambdef) is 1:
        lambdef, = lambdef
        if lambdef.name[1] == 'i':  # singleArgs
            return Fn(list(each[0] for each in lambdef), {}, (ctx, None))
        else:
            return Fn((), {}, (ctx, lambdef))

    elif len(lambdef) is 2:
        args, stmts = lambdef
        args = list(each[0] for each in args)
        return Fn(args, {}, (ctx, stmts))
    else:
        return lambda: None


def ast_for_file(file_source_parsed: 'Ast', ctx: 'ReferenceDict'):
    if file_source_parsed:
        return ast_for_statements(file_source_parsed[0], ctx)


def rem_eval(ast: 'Ast', env: 'ReferenceDict'):
    ast_for_file(ast, env)
    return env


class Fn:
    __slots__ = ['uneval_args', 'eval_args', 'body', 'just_raise']

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
