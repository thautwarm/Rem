from Ruikowa.ErrorFamily import handle_error
from Ruikowa.ObjectRegex.MetaInfo import MetaInfo
from remlang.compiler.ast import ast_for_file
from rem_parser import *
import argparse
from cytoolz import curry

cmdparser = argparse.ArgumentParser(description='Test Parser Generated by EBNFParser.')
cmdparser.add_argument("Parser", type=str,
                       help='What kind of parser do you want to test with?(e.g Stmt, Expr, ...)')
cmdparser.add_argument("Codes", metavar='lispCodes', type=str,
                       help='Input some codes in your language here.')
cmdparser.add_argument("-testTk", default=False, type=bool)
cmdparser.add_argument("-o", default="", type=str)

args = cmdparser.parse_args()
meta = MetaInfo()
parser = handle_error(eval(args.Parser))

tokenized = token(args.Codes)
if args.testTk:
    print(tokenized)

res = parser(tokenized, meta=meta, partial=False)
d = {'print': curry(print), 'list': list}
result = ast_for_file(res, d)
print(result)
if args.o:
    import json

    with open("{O}.json".format(O=args.o), 'w', encoding='utf8') as JSONFile:
        json.dump(result.dumpToJSON(), JSONFile, indent=4)
    with open("{O}".format(O=args.o), 'w', encoding='utf8') as OriginAstFile:
        OriginAstFile.write(result.dump())