
import re
import re
from typing import List
from .utils import *

e = re.escape
_keywords = [
    'then',
    'when',
    'and',
    'or',
    'in',
    'not',
    'case',
    'as',
    'end',
    'where',
    'from',
    'yield',
    'into',
    'let',
    'True',
    'False',
    'None',
    'import',
    'is'
]

keywords_map = dict(zip(_keywords, map(lambda x: f'`{x}`', _keywords)))
keywords = re.compile('|'.join(keywords_map.values()))
symbol = re.compile(
    '[a-zA-Z\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff_]{1}[a-zA-Z\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff\d_]*')
number = re.compile('0[Xx][\da-fA-F]+|\d+(?:\.\d+|)(?:E-{0,1}\d+|)')
newline = re.compile('\n+')
comment_sign = re.compile(r'(#.*)|(((/\*)+?[\w\W]+?(\*/)+))')
string = re.compile(r'"([^\\"]+|\\.)*"')
others = re.compile("|".join([
    e('=>'), e('->'), e(','), e(';'), e(':'), e("'"),

    e('++'), e('--'), e('**'), e('//'),
    e('+'), e('-'), e('*'), e('/'),

    e('%'), e('|>'), e('<-'), e('=>'),

    e('??'), e('<<'), e('>>'), e('=='),
    e('<='), e('>='), e('!='), e('$'), e('@'),
    e('?'), e('<'), e('>'), e('='),

    e('^^'), e('&&'), e('||'), e('!!'),
    e('^'), e('&'), e('|'), e('!'),
    e('...'), e('.'),

    e('{'), e('}'), e('['), e(']'),
    e('('), e(')'),

]))

tokenizer = (keywords, symbol, number, newline, string, others)


def token(inp: str) -> List[str]:
    if not inp:
        return ()

    inp = comment_sign.sub('', inp).strip(' \t\r')
    while True:
        for i, each in enumerate(tokenizer):
            m = each.match(inp)
            if m:
                w = m.group()
                if w in keywords_map:
                    yield keywords_map[w]
                else:
                    yield w
                inp = inp[m.end():].strip(' \t\r')
                if not inp:
                    return
                break
        else:
            print(inp.encode())
            raise Exception('wrong token')

