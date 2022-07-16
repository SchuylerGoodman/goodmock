from goodmock.setup import Setup

class MethodMockData:
    def __init__(self, setup : Setup):
        self._setup = setup
        self._calls = 0

    @property
    def setup(self) -> Setup:
        return self._setup

    @property
    def calls(self) -> int:
        return self._calls

    def call(self) -> int:
        self._calls += 1
        return self.calls