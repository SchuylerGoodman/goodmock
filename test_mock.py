import inspect

from typing import Any, Callable, Dict, Generic, NewType, Protocol, Type, TypeVar
from unittest import result

T = TypeVar('T')

class A:
    def __init__(self, ignore : int):
        pass

    def do1(self, a : int):
        print(a)

    def do2(self, a : int, b : str):
        print(a, b)

    def do3(self, a : int) -> int:
        print(a)
        return a


def make_init() -> None:
    def mocked_init(self):
        print('init')

    return mocked_init


def make_mocked_method(method : Type[T]) -> T:
    sig = inspect.signature(method)

    def mocked_method(*args, **kwargs):
        ba = sig.bind(*args, **kwargs)
        print('printing bound arguments', ba)

    return mocked_method


def make_mock(t : Type[T]) -> T:
    mocked_methods = {}
    for method in inspect.getmembers(t):
        if (inspect.isfunction(method[1])):
            mock_method = None
            if method[0] == '__init__':
                mock_method = make_init()
            else:
                mock_method = make_mocked_method(method[1])

            mocked_methods[method[0]] = mock_method

    mock_type = type(f'mock_{t.__name__}', (t, ), mocked_methods)
    print(mock_type)
    return mock_type()


class Mock:
    @staticmethod
    def For(mock_type : Type[T]) -> T:
        mocked_methods = {}
        for method in inspect.getmembers(mock_type):
            if (inspect.isfunction(method[1])):
                mock_method = None
                if method[0] == '__init__':
                    mock_method = make_init()
                else:
                    mock_method = Mock._make_mocked_method(method[1])

                mocked_methods[method[0]] = mock_method

        mocked_type = type(f'mock_{mock_type.__name__}', (mock_type, ), mocked_methods)
        return mocked_type()

    @staticmethod
    def _make_mocked_method(method : Type[T]) -> T:
        sig = inspect.signature(method)

        def returns(self, return_value : sig.return_annotation) -> None:
            self.return_vals
            return_val = return_value

        def mocked_method(*args, **kwargs):
            ba = sig.bind(*args, **kwargs)
            print('printing bound arguments', ba)

        return mocked_method


#P = ParamSpec('P')
R = TypeVar('R')


class MockedMethod(Callable[[T], R]):
    """
    I wanted this to enable an NSubstitute-like interface like

    mock_class = Mock.For(class_type)
    mock_class.class_method(some, input).returns(some_value)
    ...
    output_value = mock_class.class_method(some, input)
    assert output_value == some_value

    What I can't figure out is how to create a mock method with a `returns` function that
    is actually part of the static signature of `class_method` on the type returned by `Mock.For`

    I'm going to try something more like Moq, with a Mock class generic
    """
    def __init__(self, method_to_mock : Callable[[T], R]):
        self._method_to_mock = method_to_mock
        self._results = {}
        print(type(method_to_mock))

    def __call__(self, t : T) -> R:
        print('__call__', t)

        if t in self._results:
            return self._results[t]

        def returns(self, return_value : R) -> None:
            print('will return', return_value)

        results_methods = {
            'returns': returns
        }

        result = R()

        self._results[t] = 1 #MockedResult(R)

        return self._results[t]



mock_a = make_mock(A)
mock_a.do1(1)
mock_a.do2(1, 'blah')

mock_b = Mock.For(A)
mock_b.do1(1)
mock_b.do2(1, 'blah')
b_do3 = mock_b.do3(1)
print('b_do3', b_do3)

def method_to_mock(a : int):
    print(a)

mocked_method = make_mocked_method(method_to_mock)
mocked_method(1)

m = MockedMethod(method_to_mock)
m(1)
