from dataclasses import dataclass
from goodmock.when import _When
from typing import ParamSpec, TypeVar


Params = ParamSpec('Params')
TReturn = TypeVar('TReturn')


@dataclass(init=False)
class _MockType:
    when : _When[Params, TReturn]
