from .compiler.ast import (BreakUntil, handle_error, MetaInfo,
                           ast_for_statement, main)
from .standard.default import LICENSE_INFO
from .compiler.rem_parser import statement
from .console import Colored
from Ruikowa.ErrorFamily import DSLSyntaxError
from pprint import pformat
import logging
import warnings

warnings.filterwarnings("ignore")
logger = logging.Logger('irem')


def repl():
    print(Colored.Purple2, LICENSE_INFO)
    left = []
    count = None

    parser = handle_error(statement)
    while True:
        try:
            inp = input(Colored.Yellow + '>> ' if count is None else '   ')
            if not inp:
                continue
            if inp == ':manager':
                print(Colored.LightBlue, pformat(main.module_manager))
                continue
            elif inp == ':modules':
                print(Colored.LightBlue, pformat(main.module_manager['@modules']))
                continue
            elif inp == ':vars':
                print(Colored.Purple2, pformat(main))
                continue
        except KeyboardInterrupt:
            import sys
            print(Colored.Green, '\n   Good Bye~')
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
                if ret is not None and not isinstance(ret, BreakUntil):
                    print(Colored.Green, '=> ', end='')
                    if any(map(lambda x: isinstance(ret, x),
                               (list, dict, set))):  # mutable
                        print(Colored.Blue, pformat(ret))
                    elif any(map(lambda x: isinstance(ret, x),
                                 (str, int, float, complex, tuple))):  # immutable
                        print(Colored.LightBlue, pformat(ret))
                    else:
                        print(Colored.Purple, pformat(ret))

            except BaseException as e:
                logger.error(e, exc_info=True)
                print(Colored.Red, e.__class__.__name__ + ':', str(e))
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
