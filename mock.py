import inspect


from goodmock.methodmock import _MethodMock
from goodmock.methodmockcontext import _MethodMockContext
from goodmock.mocktype import _MockType
from goodmock.when import _When
from goodmock.whencontext import _WhenContext
from types import new_class
from typing import Callable, ParamSpec, Type, TypeVar, Union


TMock = TypeVar('TMock')
Params = ParamSpec('Params')
TReturn = TypeVar('TReturn')


class Mock:
    @classmethod
    def when(cls, method : _MethodMock[Params, TReturn]) -> _When[Params, TReturn]:
        if not isinstance(method, _MethodMock):
            raise Exception(f'Input method must be bound to a mock instance. Try instantiating a mock with classmock = Mock.of(ClassType) and then mocking a method call with Mock.when(classmock.{method.__name__}).')

        return method.when

    @classmethod
    def of(cls, mockedtype : Type[TMock]) -> TMock:
        mockedmembers = {}
        for membername, member in inspect.getmembers(mockedtype):
            if (inspect.isfunction(member)):
                if membername == '__init__':
                    member = Mock.__makenoopmock(member)
                else:
                    member = Mock.__makemockedmethod(member)

            mockedmembers[membername] = member

        mocktype : Union[_MockType, mockedtype] = new_class(
            f'mock_{mockedtype.__name__}',
            (_MockType, mockedtype, ),
            exec_body=lambda ns : ns.update(mockedmembers))

        mock = object.__new__(mocktype)
        mock.when = None

        return mock

    @staticmethod
    def __makenoopmock(method : Callable[Params, TReturn]) -> Callable[Params, TReturn]:
        def noopmock(*args : Params.args, **kwargs : Params.kwargs) -> TReturn:
            raise Exception(f'Cannot call method {method.__name__} on mock')

        return noopmock

    @staticmethod
    def __makemockedmethod(method : Callable[Params, TReturn]) -> Callable[Params, TReturn]:
        methodname = method.__name__
        signature = inspect.signature(method)
        parameterswithoutself = [ param for param in signature.parameters.values() if param.name != 'self' ]
        signature = signature.replace(parameters=parameterswithoutself)
        when = _When(_WhenContext(methodname, signature))
        context = _MethodMockContext(method, methodname, signature, when)

        return _MethodMock(context)
