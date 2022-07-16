from enum import Enum

class MockState(Enum):
    RESET = 0
    SETUP = 1
    VERIFY = 2

    def insetup(self):
        return self == MockState.SETUP

    def inverify(self):
        return self == MockState.VERIFY
