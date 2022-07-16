import inspect

from goodmock.methodmockdata import MethodMockData
from goodmock.mockstate import MockState
from goodmock.setup import Setup
from goodmock.returns import Returns
from typing import Callable, Dict, Generic, Type, TypeVar

TMock = TypeVar('TMock')
TReturn = TypeVar('TReturn')
TMockedMethod = TypeVar('TMockedMethod')

class Mock(Generic[TMock]):
    """
    mock_class = Mock(A)
    mock_class.setup(lambda a : a.do3(1)).returns(2)
    ...
    output = mock_class.object.do3(input_value)
    assert output == 2
    """

    def __init__(self, mockedtype : Type[TMock]) -> None:
        self._mockedtype = mockedtype
        self._object : TMock = None
        self._currentsetup = None
        self._state : MockState = MockState.RESET
        self._methoddata : Dict[str, MethodMockData] = {}
        self._timescalled : int = 0
        self._verified : bool = False

    def setup(self, mock_expr : Callable[[TMock], TReturn]) -> Setup:
        self._state = MockState.SETUP
        mock_expr(self.object)

        if self._currentsetup is None:
            raise Exception('The setup failed to initialize')
        
        setup = self._currentsetup
        self._currentsetup = None

        self._state = MockState.RESET

        return setup

    def verify(self, mock_expr : Callable[[TMock], TReturn], timescalled : int = 1) -> bool:
        self._state = MockState.VERIFY
        self._timescalled = timescalled
        mock_expr(self.object)
        self._timescalled = 0
        verified = self._verified
        self._verified = False
        self._state = MockState.RESET

        return verified

    @property
    def object(self) -> TMock:
        if self._object is None:
            self._object = self._makemock()

        return self._object

    def _makeinit(self) -> None:
        def mockedinit(self):
            raise Exception('Cannot call __init__ on mock')

        return mockedinit

    def _makemockedmethod(self, method : TMockedMethod) -> TMockedMethod:
        sig = inspect.signature(method)

        def mockedmethod(*args, **kwargs):
            ba = sig.bind(*args, **kwargs)
            methodhash = f'{method}_{Mock._hasharguments(ba, omitself=True)}'

            if self._state.insetup():
                self._currentsetup = Setup(self._mockedtype, sig.return_annotation, method, ba.arguments)
                methoddata = MethodMockData(self._currentsetup)
                self._methoddata[methodhash] = methoddata
            elif self._state.inverify():
                self._verified = self._timescalled == self._methoddata[methodhash].calls
            elif methodhash in self._methoddata: #these arguments have a registered return value
                self._methoddata[methodhash].call()
                setup = self._methoddata[methodhash].setup
                if isinstance(setup, Returns):
                    return setup.returnvalue
            else:
                raise Exception(f'This method has not been set up. Call Mock({self._mockedtype.__name__}).Setup(lambda mockobject: mockobject.{method.__name__}(...))')

            return

        return mockedmethod

    def _makemock(self) -> TMock:
        mockedmethods = {}
        for method in inspect.getmembers(self._mockedtype):
            if (inspect.isfunction(method[1])):
                mockmethod = None
                if method[0] == '__init__':
                    mockmethod = self._makeinit()
                else:
                    mockmethod = self._makemockedmethod(method[1])

                mockedmethods[method[0]] = mockmethod

        mocktype = type(f'mock_{self._mockedtype.__name__}', (self._mockedtype, ), mockedmethods)
        return object.__new__(mocktype)

    
    @staticmethod
    def _hasharguments(arguments : inspect.BoundArguments, omitself : bool = True) -> str:
        keys = []
        for (key, value) in arguments.arguments.items():
            if omitself and key == 'self':
                continue

            keys.append(key)
            keys.append(str(value))

        hash = '_'.join(keys)

        return hash