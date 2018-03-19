import argparse
import os

from remlang.compiler.err import Trace
from .compiler.ast import rem_eval, MetaInfo, rem_parser
from .intepreter import repl, main
from .console import Colored


def execute(src: str, env: dict, path: str):
    rem_eval(env['__compiler__']
        .from_source_code(
        path,
        src,
        meta=MetaInfo(fileName=path)),
        main)


def run():
    cmdparser = argparse.ArgumentParser(
        description='Rem Langauge executing tool')

    cmdparser.add_argument("--repl",
                           help='run interactive rem intepreter.',
                           default=False, nargs='?',
                           const=True)

    cmdparser.add_argument('file',
                           metavar='file',
                           default='',
                           nargs='*',
                           type=str,
                           help='input .rem source file')

    cmdparser.add_argument('-c',
                           default='',
                           nargs='?',
                           help='run some source codes',
                           type=str)

    args = cmdparser.parse_args()
    if args.repl:
        repl()
    elif args.c:
        execute(args.c, main, '<eval-input>')
    elif args.file:
        with open(args.file[0], 'r') as f:
            src = f.read()

        execute(src, main, os.path.abspath(args.file[0]))


    else:
        cmdparser.print_help()
