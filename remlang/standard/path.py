import os
from .curry import curry


class Path:
    @classmethod
    def list_dir(cls, path):
        return os.listdir(path)

    @classmethod
    def abs(cls, path):
        return os.path.abspath(path)

    @classmethod
    def combine(cls, neck, end):
        return os.path.join(neck, end)

    @classmethod
    def ext(cls, path):
        return os.path.splitext(path)[1]

    @classmethod
    def except_ext(cls, path):
        return os.path.splitext(path)[0]

    @classmethod
    def location(cls, path):
        return os.path.split(os.path.abspath(path))[0]
