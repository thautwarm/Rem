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
    '然后': ('keyword', 'then'),
    '当': ('keyword', 'when'),
    '且': ('keyword', 'and'),
    '或': ('keyword', 'or'),
    '含于': ('keyword', 'in'),
    '非': ('keyword', 'not'),
    '对于': ('keyword', 'case'),
    '作为': ('keyword', 'as'),
    '结束': ('keyword', 'end'),
    '其中': ('keyword', 'where'),
    '从': ('keyword', 'from'),
    '生成': ('keyword', 'yield'),
    '跳跃到': ('keyword', 'into'),
    '使': ('keyword', 'let'),
    '让': ('keyword', 'let'),
    '真': ('keyword', 'True'),
    '假': ('keyword', 'False'),
    '空': ('keyword', 'None'),
    '导入': ('keyword', 'import'),
    '是': ('keyword', 'is'),
    '的': ('keyword', '.'),
    '之': ('keyword', '.'),
    '等于': ('keyword', '='),
    '它': ('symbol', '_')
}
chinese_keywords = {k: (unique_literal_cache_pool[t], unique_literal_cache_pool[v])
                    for k, (t, v) in
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
