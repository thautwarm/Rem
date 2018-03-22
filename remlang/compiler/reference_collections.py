from typing import Optional


class ReferenceDict:
    __slots__ = ['local', 'module_manager', 'parent', ]

    def __init__(self, src, parent: 'Optional[ReferenceDict]' = None, module_manager=None):
        self.local = src
        self.local['__env__'] = self

        self.module_manager = module_manager

        self.parent = parent

        self.module_manager = module_manager

    def __getitem__(self, item):
        return self.local[item]

    def __setitem__(self, key, value):
        self.local[key] = value

    def get_local(self, item):
        return self.local.get(item)

    def get_nonlocal(self, item):
        now = self
        try:
            while item not in now.local:
                now = now.parent
            return now.local[item]

        except AttributeError:
            raise NameError(item)

    def set_local(self, key, value):
        self.local[key] = value

    def set_nonlocal(self, key, value):
        now = self
        try:
            while key not in now.local:
                now = now.parent
            now.local[key] = value

        except AttributeError:
            raise NameError(key)

    def get_nonlocal_env(self, item):
        now = self
        try:
            while item not in now.local:
                now = now.parent
            return now.local

        except AttributeError:
            raise NameError(item)

    def __contains__(self, item):
        return item in self.local

    def copy(self):
        return ReferenceDict(self.local.copy(), self.parent, module_manager=self.module_manager)

    def branch(self):
        return ReferenceDict({}, self, module_manager=self.module_manager)

    def branch_with(self, catch: dict):
        return ReferenceDict(catch, self, module_manager=self.module_manager)

    def update(self, *args, **kwargs):
        self.local.update(*args, **kwargs)

    def __str__(self):
        return "ReferenceDict[{}]".format(self.local.__str__())


class ParameterProxy:
    __slots__ = ['host', 'catch']

    def __init__(self, dictionary: dict, catch: dict = None):
        self.host = dictionary
        self.catch = catch if catch else {}

    def __setitem__(self, key, value):
        self.catch[key] = value

    def __getitem__(self, item):
        return self.host[item]

    def update(self, *args, **kwargs):
        self.catch.update(*args, **kwargs)

    def copy(self):
        new = ParameterProxy(self.host, self.catch.copy())
        return new

    def __contains__(self, item):
        return self.host.__contains__(item)


class ReferenceIter:
    __slots__ = ['c']
    empty = iter(())

    def __init__(self, c):
        self.c = iter(c)

    def __next__(self):
        return next(self.c)

    def __iter__(self):
        yield from self.c

    def clear(self):
        self.c = ReferenceIter.empty
