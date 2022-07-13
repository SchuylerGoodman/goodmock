import inspect
from typing import Callable, Generic, Type, TypeVar


T = TypeVar('T')
R = TypeVar('R')


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


class Returns(Generic[T], Generic[R]):
    def __init__(self, t_mock : Type[T], t_result : Type[R]) -> None:
        self._returns = None

    def returns(self, value : R) -> None:
        self._returns = value


class Setup(Returns):
    def __init__(self, t_mock : Type[T], t_result : Type[R]) -> None:
        super().__init__(t_mock, t_result)


class Mock(Generic[T]):
    """
    mock_class = Mock(A)
    mock_class.setup(lambda a : a.do3(1)).returns(2)
    ...
    output = mock_class.object.do3
    assert output == 1
    """
    def __init__(self, t : Type[T]) -> None:
        self._object : T = None
        self._in_setup = False

    def setup(self, mock_expr : Callable[[T], R]) -> Setup:
        setup = Setup(Type[T], Type[R])

        self._in_setup = True
        mock_expr(self.object)
        self._in_setup = False
        return setup

    @property
    def object(self) -> T:
        if self._object is None:
            self._object = self._make_mock(Type[T])

        return self._object

    def _make_init(self) -> None:
        def mocked_init(self):
            print('init')

        return mocked_init

    def _make_mocked_method(self, method : Type[T]) -> T:
        sig = inspect.signature(method)

        def mocked_method(*args, **kwargs):
            ba = sig.bind(*args, **kwargs)
            print('printing bound arguments', ba)

            if self._in_setup:
                pass
            #   register argument values to prep for returns
            #elif these arguments have a registered return value
            #   return it
            else:
                raise Exception('This method has not been set up')

        return mocked_method

    def _make_mock(self, t : Type[T]) -> T:
        mocked_methods = {}
        for method in inspect.getmembers(t):
            if (inspect.isfunction(method[1])):
                mock_method = None
                if method[0] == '__init__':
                    mock_method = self._make_init()
                else:
                    mock_method = self._make_mocked_method(method[1])

                mocked_methods[method[0]] = mock_method

        mock_type = type(f'mock_{t.__name__}', (t, ), mocked_methods)
        print(mock_type)
        return mock_type()




m1 = Mock(A)
s = m1.setup(lambda a : a.do3(1))
print(s)
s.returns(2)
print(m1.object.do3)