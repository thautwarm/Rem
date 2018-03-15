from .compiler.ast import (default_env, handle_error, MetaInfo,
                           ast_for_statement)
from .compiler.rem_parser import statement
from Ruikowa.ErrorFamily import DSLSyntaxError
import logging
from .standard.default import LICENSE_INFO
import warnings

warnings.filterwarnings("ignore")

logger = logging.Logger('catch_all')
main = default_env['main']



def repl():
    print(LICENSE_INFO)
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
            print('\n    Good Bye~')
            sys.exit(0)

        meta = MetaInfo(fileName='<repr>')

        left.extend(main['__token__'](inp))
        try:
            stmt = parser(left, meta=meta, partial=True)
            if meta.count != len(left):
                raise DSLSyntaxError
            try:
                left.clear()
                if count is not None:
                    count = None
                ret = ast_for_statement(stmt, main)
                if ret is not None:
                    print('=> ', repr(ret))

            except BaseException as e:
                logger.error(e, exc_info=True)
                continue

        except DSLSyntaxError:

            now_count = meta.max_fetched
            is_incremental = count is None or now_count > count

            if is_incremental:
                count = now_count
            else:
                left.clear()
                count = None
                continue
