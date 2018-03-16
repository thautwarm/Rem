try:
    from cytoolz import curry
except ModuleNotFoundError:
    from toolz import curry


@curry
def open_do(file_name, mode):
    return open(file_name, mode)


@curry
def write(content, f):
    file = f('w')
    with file:
        file.write(content)


@curry
def read(f):
    with f('r') as file:
        return file.read()
