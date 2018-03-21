if False:
    from ..compiler.module import ModuleAgent


def apply_module(module: 'ModuleAgent'):
    from ..compiler.module import ModuleAgent
    if not isinstance(module, ModuleAgent):
        raise TypeError
    return lambda ctx: ctx.update(module._)
