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
cmd_parser.add_argument('--test', nargs='?', type=bool, default=False, const=True)

warnings.filterwarnings("ignore")
logger = logging.Logger('irem')


class ReplIncompleteException(Exception):
    pass


_input = input


def repl():
    args = cmd_parser.parse_args()

    # preload sys
    ast_for_file(main['__compiler__']
                 .from_source_code('<preload>',
                                   "import sys;sys'path'append \"./\";",
                                   meta=MetaInfo(fileName='<preload>'),
                                   partial=False), main)

    testing = args.test
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
            src.clear()
            errs.clear()
            count = None
            print()
            continue

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
        elif inp == ':q':
            print(Colored.Green, '\n   Good Bye~')
            import sys
            return "End Rem Session."

        meta = MetaInfo(fileName='<repr>')
        src.append(inp)
        try:
            ans = main['__compiler__'].from_source_code('<eval input>',
                                                        '\n'.join(src),
                                                        meta=meta,
                                                        partial=False, print_token=testing)
            if testing:
                print(ans)
            try:
                ans = ast_for_file(ans, main)
                if testing:
                    print(ans)
                main['ans'] = ans
                if count is not None:
                    count = None
                if ans is not None and not isinstance(ans, BreakUntil):
                    print(Colored.Green, '=> ', end='')
                    if any(map(lambda x: isinstance(ans, x),
                               (list, dict, set))):  # mutable
                        print(Colored.Blue, pformat(ans))
                    elif any(map(lambda x: isinstance(ans, x),
                                 (str, int, float, complex, tuple))):  # immutable
                        print(Colored.LightBlue, pformat(ans))
                    else:
                        print(Colored.Purple, pformat(ans))

            except BaseException as e:
                if testing:
                    logging.error(Colored.LightBlue + str(e) + Colored.Clear, exc_info=True)
                else:
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
                    if testing:
                        logging.error(Colored.LightBlue + str(e) + Colored.Clear, exc_info=True)
                    else:
                        logger.error(Colored.LightBlue + str(e) + Colored.Clear)
                errs.clear()
                continue
