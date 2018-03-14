import re
from typing import List


def cast(to_type):
    def wrap_fn(func):
        def call(*args, **kwargs):
            return to_type(func(*args, **kwargs))

        return call

    return wrap_fn


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
    'None'
]

keywords_map = dict(zip(_keywords, map(lambda x: f'`{x}`', _keywords)))

keywords = re.compile('|'.join(keywords_map.values()))
symbol = re.compile('[a-zA-Z\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]{1}[a-zA-Z\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff\d_]*')
number = re.compile('0[Xx][\da-fA-F]+|\d+(?:\.\d+|)(?:E-{0,1}\d+|)')
newline = re.compile('\n+')
comment_sign = re.compile(r'(#.*)|(((/\*)+?[\w\W]+?(\*/)+))')
string = re.compile(r"^\"([^\"]+)\"")
others = re.compile("|".join([
    e('=>'), e('->'), e(','), e(';'), e('_'), e(':'),

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


@cast(tuple)
def token(inp: str) -> List[str]:
    if not inp:
        return ()

    inp = comment_sign.sub('', inp).strip(' ')
    while True:
        for i, each in enumerate(tokenizer):
            m = each.match(inp)
            if m:
                w = m.group()
                if w in keywords_map:
                    yield keywords_map[w]
                else:
                    yield w
                inp = inp[m.end():].strip(' ')
                if not inp:
                    return
                break
        else:
            raise Exception('wrong token:', inp.encode())


if __name__ == '__main__':
    print(token(
        """
    fn = {| x, y |
    
        x + y
    
    }
        """
    ))
