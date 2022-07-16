


from dataclasses import dataclass
from goodmock.event.stateevent import StateEventArgs, StateEventHandler


@dataclass
class VerifyStateEventArgs(StateEventArgs):
    verified : bool


class VerifyStateEventHandler(StateEventHandler[VerifyStateEventArgs]):
    def __init__(self, outeventargs : VerifyStateEventArgs) -> None:
        self._outeventargs : VerifyStateEventArgs = outeventargs

    def invoke(self, eventargs : VerifyStateEventArgs) -> None:
        self._outeventargs.verified = eventargs.verified

