from goodmock.context.mockcontext import MockContext
from goodmock.state.mockstate import MockState
from typing import Any, Callable, Dict, Type, TypeVar


TReturn = TypeVar('TReturn')


class BaseMockState(MockState[MockContext]):
    def do(self, method : Callable, arguments : Dict[str, Any], returntype : Type[TReturn], mockcontext : MockContext) -> TReturn: ...

    @staticmethod
    def hashandvalidatearguments(methodname : str, arguments : Dict[str, Any], mockcontext : MockContext, omitself : bool = True) -> str:
        methodhash = BaseMockState.hasharguments(arguments)
        if methodhash not in mockcontext[methodname]:
            raise Exception(f'This method has not been set up. Call Mock({mockcontext.mockedtype}).Setup(lambda mockobject: mockobject.{methodname}(...))')

        return methodhash

    @staticmethod
    def hasharguments(arguments : Dict[str, Any], omitself : bool = True) -> str:
        keys = []
        for (key, value) in arguments.items():
            if omitself and key == 'self':
                continue

            keys.append(key)
            keys.append(str(value))

        hash = '_'.join(keys)

        return hash
