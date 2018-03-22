from .curry import curry


@curry
def open_file(file_name, mode):
    return open(file_name, mode)


@curry
def write(f, content):
    file = f('w')
    with file:
        file.write(content)


@curry
def read(f):
    with f('r') as file:
        return file.read()


@curry
def append(f, content):
    file = f('a')
    with file:
        file.write(content)
