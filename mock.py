import inspect


from goodmock.context.mockcontext import MockContext
from goodmock.event.setupstateevent import SetupStateEventArgs, SetupStateEventHandler
from goodmock.event.verifystateevent import VerifyStateEventArgs, VerifyStateEventHandler
from goodmock.setup import Setup
from goodmock.state.callmockstate import CallMockState
from goodmock.state.setupmockstate import SetupMockState
from goodmock.state.verifymockstate import VerifyMockState
from typing import Callable, Generic, Type, TypeVar


TMock = TypeVar('TMock')
TReturn = TypeVar('TReturn')
TMockedMethod = TypeVar('TMockedMethod', bound=Callable)


class Mock(Generic[TMock]):
    """
    mock_class = Mock(A)
    mock_class.setup(lambda a : a.do3(1)).returns(2)
    ...
    output = mock_class.object.do3(input_value)
    assert output == 2
    """

    def __init__(self, mockedtype : Type[TMock]) -> None:
        self._object : TMock = None
        self._context : MockContext = MockContext(mockedtype)
        self._context.state = CallMockState()

    def setup(self, mock_expr : Callable[[TMock], TReturn]) -> Setup:
        setupstateeventargs = SetupStateEventArgs(None)
        self._context.state = SetupMockState(SetupStateEventHandler(setupstateeventargs))
        mock_expr(self.object)

        return setupstateeventargs.setup

    def verify(self, mock_expr : Callable[[TMock], TReturn], timescalled : int = 1) -> bool:
        verifystateeventargs = VerifyStateEventArgs(False)
        self._context.state = VerifyMockState(timescalled, VerifyStateEventHandler(verifystateeventargs))
        mock_expr(self.object)

        return verifystateeventargs.verified

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
            return self._context.state.do(method, ba.arguments, sig.return_annotation, self._context)

        return mockedmethod

    def _makemock(self) -> TMock:
        mockedmethods = {}
        for method in inspect.getmembers(self._context.mockedtype):
            if (inspect.isfunction(method[1])):
                mockmethod = None
                if method[0] == '__init__':
                    mockmethod = self._makeinit()
                else:
                    mockmethod = self._makemockedmethod(method[1])

                mockedmethods[method[0]] = mockmethod

        mocktype = type(f'mock_{self._context.mockedtype.__name__}', (self._context.mockedtype, ), mockedmethods)
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
