from Ruikowa.Bootstrap import Ast
from .compiler.ast import ast_for_statement, op_priority
from .compiler.rem_parser import file, statement, token
from Ruikowa.ErrorFamily import handle_error, DSLSyntaxError
from Ruikowa.ObjectRegex.MetaInfo import MetaInfo

default_env = {
    'list': list,
    'tuple': tuple,
    'max': max,
    'min': min,
    'print': print,
    'OperatorPriority': op_priority
}


def repl(env: dict = default_env):
    left = []
    count = None

    parser = handle_error(statement)
    while True:
        meta = MetaInfo(fileName='<repr>')
        try:
            inp = input('>> ' if count is None else '   ')
            if not inp:
                continue
        except KeyboardInterrupt:
            import sys
            print('Good Bye~')
            sys.exit(0)

        left.extend(token(inp))

        try:
            stmt = parser(left, meta=meta, partial=False)
            try:
                left.clear()
                if count is not None:
                    count = None
                ret = ast_for_statement(stmt, env)
                if ret is not None:
                    print('=> ', ret)

            except Exception as e:
                print(e)
                continue

        except DSLSyntaxError:

            now_count = meta.count
            is_incremental = now_count == count or count is None

            if is_incremental:
                count = now_count
            else:
                left.clear()
                count = None
                continue
