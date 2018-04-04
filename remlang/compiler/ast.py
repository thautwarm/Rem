import itertools
from Ruikowa.ObjectRegex.ASTDef import Ast
from Ruikowa.ErrorHandler import ErrorHandler
from Ruikowa.ObjectRegex.MetaInfo import MetaInfo

from .reference_collections import ReferenceDict, ParameterProxy
from .order_dual_opt import order_dual_opt, BinExp, bin_op_fns
from .rem_parser import file, token_table, UNameEnum, Tokenizer
from .utils import flatten
from .module import default_env, make_new_module, md5, ModuleAgent
from .pattern_matching import pattern_match_varargs, pattern_matching, unmatched, import_ast_for_expr
from .control_flow import BreakUntil, Macro
from .err import Trace
from .tk import keywords_map
from .msg import StatusConstructor

token_func = lambda _: Tokenizer.from_raw_strings(_, token_table, ({"space", "comments"}, {}), cast_map=keywords_map)
rem_parser = ErrorHandler(file.match, token_func)


# default settings. eval
def add_exec_func(to: 'ReferenceDict'):
    to['__compiler__'] = rem_parser
    to['exec'] = lambda src: ast_for_file(
        to['__compiler__'].from_source_code(
            '<eval input>',
            src,
            MetaInfo(fileName='<eval input>')),
        ctx=to)


# this is the main module
main = make_new_module('main', default_env)
add_exec_func(to=main)

const_map = {'r': True, 'a': False, 'o': None}


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
        if s_name is UNameEnum.expr:  # expr
            # RuikoEBNF:
            # expr ::=  testExpr (thenTrailer | applicationTrailer)* [where];
            if len(statement) is 2:
                # end with ';' then return None
                ast_for_expr(sexpr, ctx)
            else:
                return ast_for_expr(sexpr, ctx)

        elif s_name is UNameEnum.label:
            [symbol] = sexpr
            assert symbol.name is UNameEnum.symbol
            ctx.set_local('@label', symbol.string)

        elif s_name is UNameEnum.let:
            # RuikoEBNF:
            # let  Throw ['=' '!']
            #   ::= ['`let`'] symbol ['!' trailer+] '=' expr;
            to_new_ctx = False

            if sexpr[0].string is UNameEnum.keyword_let:
                # bind a new var in current environment(closure).
                to_new_ctx = True
                _, symbol, *trailers, expr = sexpr
            else:

                # For the readability of source codes,
                #   pattern matching using list destruction is better.
                symbol, *trailers, expr = sexpr

            res = ast_for_expr(expr, ctx)
            if not trailers:
                # let symbol = ...
                ctx.set_local(symbol.string, res) if to_new_ctx else ctx.set_nonlocal(symbol.string, res)
                return

            # let symbol 'attr = ... | let symbol ![item] = ...
            ref = ctx.get_nonlocal(symbol.string)
            *fst_n, [last] = trailers
            # `trailers` is a list of trailer.
            # RuikoEBNF:
            # trailer Throw ['[' ']' '.']
            #   ::= '[' exprCons ']' | '\'' symbol;

            for each, in fst_n:
                if each.name is UNameEnum.symbol:  # symbol
                    ref = getattr(ref, each.string)

                else:  # [exprCons]
                    item = tuple(ast_for_expr_cons(each, ctx))
                    if len(item) is 1:
                        item = item[0]
                    ref = ref[item]

            if last.name == UNameEnum.symbol:  # symbol
                # trailer = . symbol
                setattr(ref, last.string, res)
            else:
                # trailer = [exprCons]
                item = tuple(ast_for_expr_cons(last, ctx))
                if len(item) is 1:
                    item = item[0]
                ref[item] = res

            # let expr return Nothing
        elif s_name is UNameEnum.into:
            # RuikoEBNF:
            # into Throw ['`into`']
            #       ::= '`into`' symbol;
            [symbol] = sexpr
            # TODO with result
            raise BreakUntil(symbol.string)

        elif s_name is UNameEnum.importStmt:
            # RuikoEBNF:
            # importExpr
            #   ::= singleImportExpr | fromImportExpr | remImport;
            [branch] = sexpr

            if branch.name is not UNameEnum.remImport:
                exec(' '
                     .join
                     (map(lambda _: _.string,
                          flatten(
                              branch)))
                     .strip(),
                     ctx.local)
                return
            import os
            if len(branch) is 2:
                string, symbol = branch
                path = eval(string.string)
                name = symbol.string
            else:
                [string] = branch
                path = eval(string.string)
                name = os.path.split(
                    os.path.splitext(path)[0])[1]

            src_code, md5_v = md5(path)
            manager = ctx.module_manager
            managed_modules = manager['@modules']

            if md5_v == managed_modules.get(path):
                # imported and file not changed.
                # so do not import again
                return

            managed_modules[path] = md5_v
            env = make_new_module(name, manager, ctx['__compiler__'])
            add_exec_func(to=env)
            ast_for_file(env['__compiler__'].from_source_code(path, src_code, MetaInfo(fileName=path)),
                         env)
            ctx.set_local(name, ModuleAgent(env.local))

        else:
            raise TypeError('unknown statement.')
    except BreakUntil as e:
        raise e
    except Exception as e:
        raise Trace(e, statement)


def ast_for_expr(expr: 'Ast', ctx: ReferenceDict):
    """
    expr
        ::=  testExpr (thenTrailer | applicationTrailer)*
            [where];
    """
    assert expr.name is UNameEnum.expr

    if expr[0].__class__ is Tokenizer:
        return Macro(expr[1])

    if expr[-1].name is UNameEnum.where:  # where
        head, *then_trailers, where = expr
        stmts = where[0]
        ast_for_statements(stmts, ctx)

    else:
        head, *then_trailers = expr

    res = ast_for_test_expr(head, ctx)

    # """
    # thenTrailer throw ['then' T]
    #     ::= 'then' [T] testExpr;
    #
    # applicationTrailer throw ['$']
    #     ::= '$' testExpr;
    # """

    if len(then_trailers) is 1:
        [each] = then_trailers
        arg = ast_for_test_expr(each[0], ctx)
        return arg(res) if each.name is UNameEnum.thenTrailer else res(arg)

    stack = []
    for each in then_trailers:
        arg = ast_for_test_expr(each[0], ctx)
        if each.name is UNameEnum.thenTrailer:
            if stack:
                res = res(*stack)
                stack.clear()
            res = arg(res)
            continue
        stack.append(arg)
    if stack:
        res = res(*stack)

    return res


def ast_for_test_expr(test: Ast, ctx: ReferenceDict):
    """
    testExpr ::= caseExp | binExp;
    """
    assert test.name is UNameEnum.testExpr
    sexpr = test[0]
    if sexpr.name is UNameEnum.caseExp:
        res = ast_for_case_expr(sexpr, ctx)

    else:
        res = ast_for_bin_expr(sexpr, ctx)

    return res


def ast_for_case_expr(case_expr: 'Ast', ctx: 'ReferenceDict'):
    """
    caseExp Throw ['`case`', '`end`', T]
        ::= '`case`' expr [T] asExp* [otherwiseExp] [T] '`end`';
    """
    assert case_expr.name is UNameEnum.caseExp

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
        ::= ['`as`' patMany]
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

        if each.name is UNameEnum.patMany:
            many = each
        elif each.name is UNameEnum.expr:
            when = each
        elif each.name is UNameEnum.statements:
            statements = each

    try:
        new_ctx = ctx.branch()
        if many and not pattern_match_varargs(many, test_exp, new_ctx):
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
    binExp ::= factor ( (operator | 'or' | 'and' | 'in' | 'is') factor)*;
    """
    assert bin_expr.name is UNameEnum.binExp
    if len(bin_expr) is not 1:
        bin_expr = [each.string if each.__class__ is Tokenizer else each for each in bin_expr]
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
    assert factor.name is UNameEnum.factor
    unary_op: 'Tokenizer' = None
    suffix: 'Tokenizer' = None
    n = len(factor)
    if n is 3:
        unary_op, inv, suffix = factor

    elif n is 2:
        if factor[-1].name is UNameEnum.suffix:
            inv, suffix = factor
        else:
            unary_op, inv = factor
    else:
        inv, = factor

    res = ast_for_inv_exp(inv, ctx)

    if suffix:
        if suffix.string is '?':
            res = True if res else False
        else:
            # '??'
            res = res is not None

    if unary_op:
        if unary_op.string is '+':
            return res
        elif unary_op.string is '-':
            return -res
        else:  # not
            return not res

    return res


def ast_for_inv_exp(inv: 'Ast', ctx: 'ReferenceDict'):
    """
    invExp  ::= atomExpr (atomExpr | invTrailer)*;
    """
    assert inv.name is UNameEnum.invExp
    atom_expr, *inv_trailers = inv
    res = ast_for_atom_expr(atom_expr, ctx)

    if len(inv_trailers) is 1:
        [each] = inv_trailers
        if each.name is UNameEnum.atomExpr:
            return res(ast_for_atom_expr(each, ctx))
        return ast_for_atom_expr(each[0], ctx)(res)

    stack = []
    for each in inv_trailers:
        if each.name is UNameEnum.atomExpr:
            stack.append(ast_for_atom_expr(each, ctx))
            continue
        if stack:
            res = res(*stack)
            stack.clear()

        res = (ast_for_atom_expr(each[0], ctx))(res)

    if stack:
        res = res(*stack)

    return res


def ast_for_atom_expr(atom_expr: 'Ast', ctx: 'ReferenceDict'):
    """
    atomExpr Throw[T] ::= atom ([T] trailer)*;
    """
    assert atom_expr.name is UNameEnum.atomExpr
    atom, *trailers = atom_expr
    res = ast_for_atom(atom, ctx)
    try:
        for each, in trailers:
            # RuikoEBNF
            # trailer Throw ['!' '[' ']' '\'']
            #       ::= '!' '[' exprCons ']' | '\'' symbol;

            if each.name is UNameEnum.symbol:
                name = each.string
                res = getattr(res, name)
            else:
                item = tuple(ast_for_expr_cons(each, ctx))
                if len(item) is 1:
                    item = item[0]
                res = res[item]
        return res

    except BreakUntil as e:
        raise e
    except Exception as e:
        raise Trace(e, atom_expr)


def ast_for_atom(atom: 'Ast', ctx: 'ReferenceDict'):
    """
    atom  Throw ['++']
        ::=  refName | const | string ('++' string)* | number |
            '(' expr ')'|
             listCons | tupleCons | setCons | dictCons | compreh |
             lambdef;
    """
    assert atom.name is UNameEnum.atom
    if len(atom) is 1:
        sexpr = atom[0]
        s_name = sexpr.name
        if s_name is UNameEnum.refName:

            if len(sexpr) is 2:
                return RefName(sexpr[1].string)

            ret = ctx.get_nonlocal(sexpr[0].string)
            if ret.__class__ is Macro:
                return ast_for_expr(ret.expr, ctx)
            return ret

        elif s_name is UNameEnum.const:
            sign = sexpr[0].string[1]
            return const_map[sign]

        elif s_name is UNameEnum.compreh:
            # comprehension
            try:
                return ast_for_comprehension(sexpr, ctx)
            except BreakUntil as e:
                if e.name != ctx.get_local('@label'):
                    raise e

        elif s_name is UNameEnum.number:
            return eval(sexpr.string)

        elif s_name is UNameEnum.lambdef:
            return ast_for_lambdef(sexpr, ctx)

        elif s_name is UNameEnum.listCons:
            if not sexpr:
                return list()
            return list(ast_for_expr_cons(sexpr[0], ctx))

        elif s_name is UNameEnum.tupleCons:  # tupleCons
            if not sexpr:
                return tuple()
            return tuple(ast_for_expr_cons(sexpr[0], ctx))

        elif s_name is UNameEnum.string:
            return eval(sexpr.string)

        elif s_name is UNameEnum.setCons:
            if not sexpr:
                return set()
            return set(ast_for_expr_cons(sexpr[0], ctx))

        elif s_name is UNameEnum.dictCons:  # dictCons
            if not sexpr:
                return dict()
            return dict(ast_for_kv_cons(sexpr[0], ctx))

    elif atom[0].string is '(':  # '(' expr ')'
        return ast_for_expr(atom[1], ctx)

    else:  # string ('++' string)*
        return ''.join(eval(each.string) for each in atom)


def ast_for_expr_cons(expr_cons: 'Ast', ctx: 'ReferenceDict'):
    """
    exprCons Throw [',' T] ::= exprMany ([T] ',' [T] unpack [[T] ',' [T] exprMany])* [','];
    """
    for each in expr_cons:
        if each.name is UNameEnum.unpack:  # unpack
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
        if each.name is UNameEnum.unpack:  # unpack
            iterator = ast_for_expr(each[0], ctx)
            yield from iterator.items() if isinstance(iterator, dict) else iterator

        else:
            for k, v in each:
                yield ast_for_expr(k, ctx), ast_for_expr(v, ctx)


def _cps(f, xs):
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
    if comprehension[1].name is UNameEnum.keyword:
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
            return (lambdef(*each) for each in cartesian_prod_collections)

        e = None

        for each in cartesian_prod_collections:
            e = lambdef(*each)

        return e

    except BreakUntil as e:
        if e.name != ctx.get_local('@label'):
            raise e
        return e.res


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
    assert lambdef.name is UNameEnum.lambdef
    n = len(lambdef)
    if n is 1:
        lambdef, = lambdef
        if lambdef.name is UNameEnum.simpleArgs:  # singleArgs
            return Fn(list(each.string for each in lambdef), (), (), ctx)
        else:
            return Thunk(lambdef, ctx)

    elif n is 2:
        args, stmts = lambdef
        if args.name is UNameEnum.noZipPatMany:
            args = tuple(_ for [_] in args)
            ctx = ReferenceDict(ParameterProxy(ctx.local), ctx.parent, ctx.module_manager)
            return PatternMatchingFn(args, stmts, ctx)
        return Fn(list(each.string for each in args), (), stmts, ctx)
    else:
        return lambda: None


def ast_for_file(file_source_parsed: 'Ast', ctx: 'ReferenceDict'):
    if file_source_parsed:
        return ast_for_statements(file_source_parsed[0], ctx)


def rem_eval(ast: 'Ast'):
    return lambda ctx: ast_for_expr(ast, ctx)


class Thunk:
    __slots__ = ['stmts', 'ctx', 'args']

    def __init__(self, stmts, ctx):
        self.ctx: ReferenceDict = ctx
        self.stmts: Ast = stmts

    def __call__(self, *args):
        if not args:
            new_ctx = self.ctx.branch()
            return ast_for_statements(self.stmts, new_ctx)

        eval_args = {'_': args[0]}

        if len(args) > 1:
            eval_args.update({f'_{i + 1}': arg for i, arg in enumerate(args)})

        return ast_for_statements(self.stmts, self.ctx.branch_with(eval_args))


class Fn:
    __slots__ = ['uneval_args', 'eval_args', 'stmts', 'ctx']

    def __init__(self, uneval, eval_args, stmts, ctx):
        self.uneval_args = uneval
        self.eval_args = eval_args
        self.ctx = ctx
        self.stmts = stmts

    def __call__(self, *args):

        if not args:
            if self.uneval_args:
                return StatusConstructor('err')

            new_ctx: 'ReferenceDict' = self.ctx.branch()
            new_ctx.update(self.eval_args)
            return ast_for_statements(self.stmts, new_ctx)

        nargs = len(args)
        n_uneval = len(self.uneval_args)

        if nargs >= n_uneval:
            args_iter = iter(args)
            eval_args = self.eval_args + tuple(zip(self.uneval_args, args_iter))
            new_ctx: 'ReferenceDict' = self.ctx.branch()

            new_ctx.update(eval_args)

            if nargs is n_uneval:
                return ast_for_statements(self.stmts, new_ctx)
            return ast_for_statements(self.stmts, new_ctx)(*args_iter)

        uneval_args_iter = iter(self.uneval_args)
        eval_args = self.eval_args + tuple((k, v) for v, k in zip(args, uneval_args_iter))
        return Fn(tuple(uneval_args_iter), eval_args, self.stmts, self.ctx)


class PatternMatchingFn:
    __slots__ = ['uneval_pats', 'stmts', 'ctx']

    def __init__(self, uneval, stmts, ctx):
        self.uneval_pats = uneval
        self.ctx = ctx
        self.stmts = stmts

    def __call__(self, *args):
        nargs = len(args)
        n_uneval = len(self.uneval_pats)

        if nargs >= n_uneval:
            new_ctx = self.ctx.branch_with(self.ctx.local.catch)
            args_iter = iter(args)
            if not all(pattern_matching(k, v, new_ctx) for k, v in zip(self.uneval_pats, args_iter)):
                return StatusConstructor("err")

            if nargs is n_uneval:
                return ast_for_statements(self.stmts, new_ctx)
            return ast_for_statements(self.stmts, new_ctx)(*args_iter)

        new_ctx = self.ctx.copy()
        uneval_args_iter = iter(self.uneval_pats)
        if not all(pattern_matching(k, v, new_ctx) for v, k in zip(args, uneval_args_iter)):
            return StatusConstructor("err")

        return PatternMatchingFn(tuple(uneval_args_iter), self.stmts, new_ctx)


import_ast_for_expr()
