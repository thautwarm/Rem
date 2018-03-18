from Ruikowa.Bootstrap import Ast


class Trace(Exception):
    __slots__ = ['origin', 'trace']

    def __init__(self, orgin: Exception, meta: 'Ast'):
        self.origin = orgin
        self.meta = meta

    def __str__(self):
        return '{}\nerror : {} line: {} at: file {}\n'.format(self.origin,
                                                              self.origin.__class__,
                                                              self.meta[0],
                                                              self.meta[2])
