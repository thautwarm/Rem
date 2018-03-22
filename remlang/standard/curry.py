try:
    from cytoolz import curry, compose
except ModuleNotFoundError:
    from toolz import curry, compose
