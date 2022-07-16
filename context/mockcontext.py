from goodmock.context.methodmockcontext import MethodMockContext
from goodmock.state.mockstate import MockState
from typing import Dict, Type, TypeVar


TMock = TypeVar('TMock')


class MockContext(Dict[str, MethodMockContext]):
    def __init__(self, mockedtype : Type[TMock]):
        super().__init__()

        self._mockedtype = mockedtype

    @property
    def state(self) -> MockState['MockContext']:
        return self._state

    @state.setter
    def state(self, value : MockState['MockContext']) -> None:
        self._state = value

    @property
    def mockedtype(self) -> Type[TMock]:
        return self._mockedtype

    @property
    def verified(self) -> bool:
        return self._verified

    @verified.setter
    def verified(self, verified : bool) -> None:
        self._verified = verified

    def __getitem__(self, __k: str) -> MethodMockContext:
        if __k not in self:
            self[__k] = MethodMockContext()

        return super().__getitem__(__k)
