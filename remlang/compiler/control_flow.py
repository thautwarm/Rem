from Ruikowa.ObjectRegex.ASTDef import Ast
from Ruikowa.color import Colored


class BreakUntil(Exception):
    __slots__ = ['name', 'res']

    def __init__(self, name, res='ct'):
        self.name = name
        self.res = res

    def __str__(self):
        return 'BreakUntil[label name = {}] with result: {}'.format(self.name, self.res)


class Macro:
    __slots__ = ['expr']

    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f'{Colored.Green}[Macro]: \n{self.expr}\n{Colored.Clear}'

    def __repr__(self):
        return self.__str__()
