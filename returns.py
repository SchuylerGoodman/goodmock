from typing import Any, Callable, Generic, OrderedDict, Type, TypeVar

TMock = TypeVar('TMock')
TReturn = TypeVar('TReturn')

class Returns(Generic[TMock, TReturn]):
    def __init__(self, tmock : Type[TMock], tresult : Type[TReturn], method : Callable, arguments : OrderedDict[str, Any]) -> None:
        self._tmock = tmock
        self._returnvalue = None
        self._method = method
        self._arguments = arguments

    @property
    def returnvalue(self) -> TReturn:
        if (self._returnvalue is None):
            argumentstr = ', '.join([f'{k}={v}' for (k, v) in self._arguments.items()])
            raise Exception(f'No return value set up for {self._tmock.__name__}.{self._method.__name__}({argumentstr})')

        return self._returnvalue

    def returns(self, value : TReturn) -> None:
        self._returnvalue = value