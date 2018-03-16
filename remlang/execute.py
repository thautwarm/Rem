import argparse
from .compiler.ast import rem_eval, MetaInfo, rem_parser
from .intepreter import repl, main


def execute(src: str, env: dict):
    rem_eval(rem_parser(env['__token__'](src),
                        meta=MetaInfo(fileName='.'),
                        partial=False),
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
                           nargs='?',
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
        execute(args.c, main)
    elif args.file:
        with open(args.file, 'r') as f:
            src = f.read()
        execute(src, main)
    else:
        cmdparser.print_help()
