from goodmock.context.mockcontext import MockContext
from goodmock.event.verifystateevent import VerifyStateEventArgs
from goodmock.event.stateevent import StateEventHandler
from goodmock.state.basemockstate import BaseMockState
from goodmock.state.callmockstate import CallMockState
from typing import Any, Callable, Dict, Type, TypeVar


TReturn = TypeVar('TReturn')


class VerifyMockState(BaseMockState):
    def __init__(self, expectedtimescalled, verifystateeventhandler : StateEventHandler[VerifyStateEventArgs]):
        self._expectedtimescalled = expectedtimescalled
        self._verifystateeventhandler : StateEventHandler[VerifyStateEventArgs] = verifystateeventhandler

    def do(self, method : Callable, arguments : Dict[str, Any], _ : Type[TReturn], mockcontext : MockContext) -> TReturn:
        mockcontext.verified = False

        methodname = method.__name__
        methodhash = BaseMockState.hashandvalidatearguments(methodname, arguments, mockcontext)

        # verify method call count is as expected
        verified = self._expectedtimescalled == mockcontext[methodname][methodhash].calls

        # reset state to CallMockState
        mockcontext.state = CallMockState()

        # trigger verify state event
        self._verifystateeventhandler.invoke(VerifyStateEventArgs(verified))
