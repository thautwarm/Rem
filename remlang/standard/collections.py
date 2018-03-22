from .curry import curry
from collections import Iterator
from itertools import groupby


def xrange(arg):
    if not isinstance(arg, tuple):
        return range(arg)
    return range(*arg)


@curry
def chunk_by(collection, f):
    return ((v, tuple(vs)) for v, vs in groupby(collection, f))


@curry
def chunk(collection, n):
    return (tuple(x for _, x in vs) for v, vs in groupby(enumerate(collection), lambda tp: tp[0] // n))


def fst(collection):
    if isinstance(collection, Iterator):
        try:
            return next(collection)
        except StopIteration:
            return None
    try:
        return collection[0]
    except IndexError:
        return None


def snd(collection):
    if isinstance(collection, Iterator):
        try:
            return next(next(collection))
        except StopIteration:
            return None
    try:
        return collection[1]
    except IndexError:
        return None
