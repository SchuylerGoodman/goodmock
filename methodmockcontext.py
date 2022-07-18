import inspect

from dataclasses import dataclass
from goodmock.when import _When
from typing import Callable, Generic, ParamSpec, TypeVar


Params = ParamSpec('Params')
TReturn = TypeVar('TReturn')


@dataclass
class _MethodMockContext(Generic[Params, TReturn]):
    originalmethod : Callable[Params, TReturn]
    methodname : str
    signature : inspect.Signature
    when : _When[Params, TReturn]
