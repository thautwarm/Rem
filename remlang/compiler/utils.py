chinese_keywords = {
    '然后': '`then`',
    '当': '`when`',
    '并且': '`and`',
    '或者': '`or`',
    '含于': '`in`',
    '非': '`not`',
    '对于': '`case`',
    '作为': '`as`',
    '结束': '`end`',
    '其中': '`where`',
    '从': '`from`',
    '生成': '`yield`',
    '跳跃到': '`into`',
    '使': '`let`',
    '真': '`True`',
    '假': '`False`',
    '空': '`None`',
    '导入': '`import`',
    '是': '`is`'
}


def to_chinese(tokens):
    return (chinese_keywords[w] if w in chinese_keywords else w for w in tokens)


def cast(to_type):
    def wrap_fn(func):
        def call(*args, **kwargs):
            return to_type(func(*args, **kwargs))

        return call

    return wrap_fn
