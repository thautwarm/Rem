from Ruikowa.ObjectRegex.ASTDef import Ast
from Ruikowa.ObjectRegex.Tokenizer import Tokenizer
from Ruikowa.io import grace_open
from Ruikowa.ErrorFamily import find_location


class Trace(Exception):
    __slots__ = ['origin', 'tk', 'filename']

    def __init__(self, origin: Exception, statement: 'Ast'):

        tk: 'Ast' = statement
        while tk.__class__ is not Tokenizer:
            tk = tk[0]
        self.origin = origin
        self.tk: 'Tokenizer' = tk
        self.filename = statement.meta[-1]

    def __str__(self):

        try:
            src_code = grace_open(self.filename).read()
        except FileNotFoundError:
            src_code = None
        except OSError:
            src_code = None

        location = find_location(self.filename, where=self.tk, src_code=src_code)

        return f'{self.origin}\nerror : {self.origin.__class__} at {location}\n'

    def __repr__(self):
        return self.__str__()
