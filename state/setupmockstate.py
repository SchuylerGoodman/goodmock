from goodmock.context.argumentcontext import ArgumentContext
from goodmock.context.mockcontext import MockContext
from goodmock.event.setupstateevent import SetupStateEventArgs
from goodmock.event.stateevent import StateEventHandler
from goodmock.setup import Setup
from goodmock.state.basemockstate import BaseMockState
from goodmock.state.callmockstate import CallMockState
from typing import Any, Callable, Dict, Type, TypeVar


TReturn = TypeVar('TReturn')


class SetupMockState(BaseMockState):
    def __init__(self, setupstateeventhandler : StateEventHandler[SetupStateEventArgs]):
        self._setupstateeventhandler : StateEventHandler[SetupStateEventArgs] = setupstateeventhandler

    def do(self, method : Callable, arguments : Dict[str, Any], returntype : Type[TReturn], mockcontext : MockContext) -> TReturn:
        # create and set new argument context
        setup = Setup(mockcontext.mockedtype, returntype, method, arguments)
        argumentcontext = ArgumentContext(setup, 0)
        methodname = method.__name__
        methodhash = BaseMockState.hasharguments(arguments)
        mockcontext[methodname][methodhash] = argumentcontext

        # reset state to CallMockState
        mockcontext.state = CallMockState()

        # trigger setup state event
        self._setupstateeventhandler.invoke(SetupStateEventArgs(setup))
