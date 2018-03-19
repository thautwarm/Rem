from Ruikowa.ObjectRegex.Tokenizer import unique_literal_cache_pool

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
    'is',
]

keywords_map = dict(zip(_keywords, [unique_literal_cache_pool['keyword']] * len(_keywords)))
