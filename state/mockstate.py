from typing import Any, Callable, Dict, Protocol, Type, TypeVar


TContext = TypeVar('TContext')
TReturn = TypeVar('TReturn')


class MockState(Protocol[TContext]):
    def do(self, method : Callable, arguments : Dict[str, Any], returntype : Type[TReturn], mockcontext : TContext) -> TReturn: ...
