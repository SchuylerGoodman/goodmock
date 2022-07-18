from goodmock.takes import _Takes
from goodmock.whencontext import _WhenContext
from typing import Generic, ParamSpec, TypeVar


Params = ParamSpec('Params')
TReturn = TypeVar('TReturn')


class _When(Generic[Params, TReturn]):
    def __init__(self, whencontext : _WhenContext) -> None:
        self.__context = whencontext

    def takes(self, *args : Params.args, **kwargs : Params.kwargs) -> _Takes[TReturn]:
        ba = self.__context.signature.bind(*args, **kwargs)
        argstr = self.__hasharguments(True, *args, **kwargs)

        if argstr not in self.__context:
            self.__context[argstr] = _Takes()

        return self.__context[argstr]
   

    def __hasharguments(self, omitself : bool, *args : Params.args, **kwargs : Params.kwargs) -> str:
        ba = self.__context.signature.bind(*args, **kwargs)

        keys = []
        for (key, value) in ba.arguments.items():
            if omitself and key == 'self':
                continue

            keys.append(f'{key}={value}')

        hash = ','.join(keys)

        return hash
