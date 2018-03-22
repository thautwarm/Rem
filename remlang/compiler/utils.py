from collections import Iterable
from Ruikowa.ObjectRegex.Tokenizer import Tokenizer
from Ruikowa.ObjectRegex.Tokenizer import unique_literal_cache_pool
from typing import List

from ..standard.curry import curry


@curry
def map_token(mapping: dict, tk: Tokenizer):
    name, string = mapping[tk.name, tk.string]
    return Tokenizer(name, string, tk.lineno, tk.colno)


chinese_keywords = {
    '然后': 'then',
    '当': 'when',
    '并且': 'and',
    '或者': 'or',
    '含于': 'in',
    '非': 'not',
    '对于': 'case',
    '作为': 'as',
    '结束': 'end',
    '其中': 'where',
    '从': 'from',
    '生成': 'yield',
    '跳跃到': 'into',
    '使': 'let',
    '让': 'let',
    '真': 'True',
    '假': 'False',
    '空': 'None',
    '导入': 'import',
    '是': 'is',
    '之': '.',
}
chinese_keywords = {k: (unique_literal_cache_pool['keyword'], unique_literal_cache_pool[v])
                    for k, v in
                    chinese_keywords.items()}


def to_chinese(tokens: List[Tokenizer]):
    for w in tokens:
        if w.string in chinese_keywords:
            name, string = chinese_keywords[w.string]
            yield Tokenizer(name, string, w.lineno, w.colno)
        else:
            yield w


def cast(to_type):
    def wrap_fn(func):
        def call(*args, **kwargs):
            return to_type(func(*args, **kwargs))

        return call

    return wrap_fn


def flatten(seq):
    for each in seq:
        if isinstance(each, Iterable) and not isinstance(each, str):
            yield from flatten(each)
        else:
            yield each
