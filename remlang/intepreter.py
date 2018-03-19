from .compiler.ast import (BreakUntil, ErrorHandler, MetaInfo,
                           ast_for_file, main)
from .standard.default import LICENSE_INFO
from .compiler.rem_parser import statement
from .console import Colored
from Ruikowa.io import grace_open
from Ruikowa.ErrorFamily import DSLSyntaxError
from pprint import pformat
import logging
import warnings
import argparse

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument('--file', nargs='?', type=str)

warnings.filterwarnings("ignore")
logger = logging.Logger('irem')


class ReplIncompleteException(Exception):
    pass


_input = input


def repl():
    args = cmd_parser.parse_args()
    if args.file:
        file_src = iter(grace_open(args.file).read().splitlines())
        std_input = _input

        def input(s):
            code = next(file_src)
            print(s, code)
            return code
    else:
        input = _input

    print(Colored.Purple2, LICENSE_INFO, Colored.Clear)
    count = None
    src = []
    errs = []
    while True:
        try:
            inp = input(Colored.Yellow + '>> ' if count is None else '   ')
        except StopIteration:
            input = std_input
            continue
        except KeyboardInterrupt:
            import sys
            print(Colored.Green, '\n   Good Bye~')
            sys.exit(0)

        if not inp:
            continue
        elif inp == ':manager':
            print(Colored.LightBlue, pformat(main.module_manager.local))
            continue
        elif inp == ':modules':
            print(Colored.LightBlue, pformat(main.module_manager['@modules']))
            continue
        elif inp == ':vars':
            print(Colored.Purple2, pformat(main.local))
            continue

        meta = MetaInfo(fileName='<repr>')
        src.append(inp)
        try:
            ret = main['__compiler__'].from_source_code('<eval input>',
                                                        '\n'.join(src),
                                                        meta=meta,
                                                        partial=False)
            try:
                ret = ast_for_file(ret, main)

                if count is not None:
                    count = None
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
                logger.error(Colored.LightBlue + str(e) + Colored.Clear)

            src.clear()
            errs.clear()

        except DSLSyntaxError as e:
            errs.append(e)
            now_count = meta.max_fetched
            is_incremental = count is None or now_count > count

            if is_incremental:
                count = now_count
            else:
                src.clear()
                count = None
                for e in errs:
                    logger.error(Colored.LightBlue + str(e) + Colored.Clear)
                errs.clear()
                continue
