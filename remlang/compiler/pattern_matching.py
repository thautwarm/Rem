from .reference_collections import ReferenceIter

unmatched = object()


def _pattern_match(left_e, right_e, ctx):
    try:
        if left_e is '_':
            right_e.clear()
            return True

        elif left_e.name == 'refName':
            [*ref, (name,)] = left_e

            if ref:
                return ctx.get_nonlocal(name) == right_e
            else:
                ctx.set_local(name, right_e)
                return True

        elif left_e.name == 'string':
            return eval(left_e[0]) == right_e

        elif left_e.name == 'const':
            const = left_e[0]
            return {'`True`': True,
                    '`False`': False,
                    '`None`': None}[const] is right_e


        elif left_e.name == 'number':
            return eval(left_e[0]) == right_e

        elif left_e.name == 'tupleArg':
            if not left_e:
                try:
                    next(right_e)
                except StopIteration:
                    return True
                else:
                    return False
            many = left_e[0]
            return pattern_match(many, right_e, ctx)

        else:
            assert False

    except:
        return False


def pattern_match(left, right, ctx):
    try:
        is_iter: bool = False
        if left[-1].name == 'iterMark':
            left.pop()
            is_iter = True
        elif len(left) > 1:
            is_iter = True

        if not is_iter:
            # no
            return _pattern_match(left[0][-1], right, ctx)

        left = ReferenceIter(left)

        right = ReferenceIter(right)

        while True:
            try:
                k = next(left)
            except StopIteration:
                try:
                    next(right)
                    # no
                    return False
                except StopIteration:
                    # no
                    return True

            else:
                if k[0] == '...':
                    k = k[1]
                    if not _pattern_match(k, right.c, ctx):
                        # no
                        return False
                    return True

                v = next(right)
                if not _pattern_match(k[0], v, ctx):
                    # no
                    return False


    except:

        return False
