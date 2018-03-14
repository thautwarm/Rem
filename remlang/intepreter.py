from .compiler.ast import (default_env, handle_error, MetaInfo,
                           token, ast_for_statement)
from .compiler.rem_parser import statement
from Ruikowa.ErrorFamily import DSLSyntaxError
import logging

logger = logging.Logger('catch_all')
main = default_env['main']


def repl():
    left = []
    count = None

    parser = handle_error(statement)
    while True:
        try:
            inp = input('>> ' if count is None else '   ')
            if not inp:
                continue
            if inp == ':manager':
                print(main['@module_manager'])
                continue
            elif inp == ':modules':
                print(main['@module_manager']['@modules'])
                continue
            elif inp == ':vars':
                print(main)
                continue
        except KeyboardInterrupt:
            import sys
            print('Good Bye~')
            sys.exit(0)

        meta = MetaInfo(fileName='<repr>')

        left.extend(token(inp))
        try:
            stmt = parser(left, meta=meta, partial=False)
            try:
                left.clear()
                if count is not None:
                    count = None
                ret = ast_for_statement(stmt, main)
                if ret is not None:
                    print('=> ', ret)

            except BaseException as e:
                logger.error(e, exc_info=True)
                continue

        except DSLSyntaxError:

            now_count = meta.count
            is_incremental = count is None or now_count > count

            if is_incremental:
                count = now_count
            else:
                left.clear()
                count = None
                continue
