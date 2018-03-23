import argparse
import os

from remlang.compiler.err import Trace
from remlang.compiler.reference_collections import ReferenceDict
from .compiler.ast import ast_for_file, MetaInfo, rem_parser
from .intepreter import repl, main
from .console import Colored
import warnings, logging

warnings.filterwarnings("ignore")
logger = logging.Logger('rem-exec')


def execute(src: str, env: ReferenceDict, path: str):
    ast_for_file(env['__compiler__']
        .from_source_code(
        path,
        src,
        meta=MetaInfo(fileName=path)),
        env)


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
        execute("import sys; sys'path'append(\"./\");print 1", main, '<preload>')
        execute(args.c, main, '<eval-input>')
    elif args.file:
        with open(args.file[0], 'r') as f:
            src = f.read()
        try:
            execute("import sys;sys'path'append \"./\";", main, "<preload>")
            execute(src, main, os.path.abspath(args.file[0]))
        except Exception as e:
            logger.error(Colored.LightBlue + str(e) + Colored.Clear)


    else:
        cmdparser.print_help()
