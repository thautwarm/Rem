


class BreakUntil(Exception):
    __slots__ = ['name', 'res']

    def __init__(self, name, res='ct'):
        self.name = name
        self.res = res

    def __str__(self):
        return 'BreakUntil[label name = {}] with result: {}'.format(self.name, self.res)



