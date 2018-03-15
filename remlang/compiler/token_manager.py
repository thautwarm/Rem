from .utils import cast
from .rem_parser import token


class TokenManager:

    def __init__(self):
        self.token_func = token

    def set(self, token_func):
        self.token_func = token_func
        return self

    def mut_by(self, f):
        self.token_func = f(self.token_func)

    def to_default(self):
        self.token_func = token

    @cast(tuple)
    def __call__(self, inp: str):
        return self.token_func(inp)
