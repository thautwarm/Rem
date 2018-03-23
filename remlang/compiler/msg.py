class RemStatus:
    __slots__ = ['name']

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Status[{}]'.format(self.name)

    def __repr__(self):
        return self.__str__()


class StatusConstructor:
    __atom_set__ = {}

    def __new__(cls, name):

        if name in cls.__atom_set__:
            return cls.__atom_set__[name]

        status = cls.__atom_set__.get(name)

        if not status:
            status = cls.__atom_set__[name] = RemStatus(name)
            return status
        return status
