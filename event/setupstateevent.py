from dataclasses import dataclass
from goodmock.event.stateevent import StateEventArgs, StateEventHandler
from goodmock.setup import Setup


@dataclass
class SetupStateEventArgs(StateEventArgs):
    setup : Setup


class SetupStateEventHandler(StateEventHandler[SetupStateEventArgs]):
    def __init__(self, outeventargs : SetupStateEventArgs) -> None:
        self._outeventargs : SetupStateEventArgs = outeventargs

    def invoke(self, eventargs : SetupStateEventArgs) -> None:
        self._outeventargs.setup = eventargs.setup
