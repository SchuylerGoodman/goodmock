from typing import Generic, TypeVar


TReturn = TypeVar('TReturn')


class _Takes(Generic[TReturn]):
    def __init__(self):
        self.__returns : TReturn = None
        self.__raises : Exception = None

    @property
    def returns(self) -> TReturn:
        return self.__returns

    @returns.setter
    def returns(self, value : TReturn) -> None:
        if self.raises is not None:
            raise Exception('Mock cannot both return a value and raise an exception')

        self.__returns = value

    @property
    def raises(self) -> Exception:
        return self.__raises

    @raises.setter
    def raises(self, value : Exception) -> None:
        if self.returns is not None:
            raise Exception('Mock cannot both return a value and raise an exception')

        self.__raises = value
