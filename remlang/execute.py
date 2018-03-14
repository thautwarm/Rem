import argparse
from .compiler.ast import rem_eval, default_env, MetaInfo, rem_parser, token

main = default_env['main']


def execute(src):
    rem_eval(rem_parser(token(src),
                        meta=MetaInfo(fileName='.'),
                        partial=False), main)
