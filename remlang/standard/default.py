from cytoolz import curry

default = {
    'list': list,
    'tuple': tuple,
    'max': max,
    'min': min,
    'print': print,
    'get': curry(getattr)
}
