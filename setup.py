from goodmock.returns import Returns
from typing import Any, Callable, Generic, OrderedDict, Type, TypeVar

TMock = TypeVar('TMock')
TReturn = TypeVar('TReturn')

class Setup(Returns):
    def __init__(self, tmock : Type[TMock], tresult : Type[TReturn], method : Callable, arguments : OrderedDict[str, Any]) -> None:
        super().__init__(tmock, tresult, method, arguments)