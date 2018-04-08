from .curry import curry

codecs = ('utf8', 'gb18030', 'latin-1')
def try_open(filename, mode):
	for each in codecs:
		try:
			return open(filename, mode, encoding=each)
		except UnicodeDecodeError:
			continue
	raise UnicodeDecodeError

@curry
def open_file(file_name, mode):
    return try_open(file_name, mode)


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
