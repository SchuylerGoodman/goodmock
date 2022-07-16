from dataclasses import dataclass
from typing import Protocol, TypeVar


@dataclass
class StateEventArgs:
    pass


StateEventArgsType = TypeVar('StateEventArgsType', bound=StateEventArgs)


class StateEventHandler(Protocol[StateEventArgsType]):
    def invoke(self, eventargs : StateEventArgsType) -> None: ...
