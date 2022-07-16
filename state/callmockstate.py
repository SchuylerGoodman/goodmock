from goodmock.context.mockcontext import MockContext
from goodmock.state.basemockstate import BaseMockState
from goodmock.returns import Returns
from typing import Any, Callable, Dict, Type, TypeVar


TReturn = TypeVar('TReturn')


class CallMockState(BaseMockState):
    def do(self, method : Callable, arguments : Dict[str, Any], returntype : Type[TReturn], mockcontext : MockContext) -> TReturn:
        methodname = method.__name__
        methodhash = BaseMockState.hashandvalidatearguments(methodname, arguments, mockcontext)
        argumentcontext = mockcontext[methodname][methodhash]

        # increment call count
        argumentcontext.calls += 1

        # return correct return value
        setup = argumentcontext.setup
        if isinstance(setup, Returns):
            return setup.returnvalue
