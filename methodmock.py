from goodmock.methodmockcontext import _MethodMockContext
from goodmock.takes import _Takes
from goodmock.when import _When
from typing import Callable, Generic, ParamSpec, TypeVar


Params = ParamSpec('Params')
TReturn = TypeVar('TReturn')


class _MethodMock(Generic[Params, TReturn], Callable[Params, TReturn]):
    def __init__(self, methodmockcontext : _MethodMockContext[Params, TReturn]) -> None:
        self.__context = methodmockcontext

    @property
    def when(self) -> _When[Params, TReturn]:
        if not self.__context.when:
            raise Exception(f'There was an issue initializing the mock') # TODO more useful message

        return self.__context.when

    def __call__(self, *args: Params.args, **kwds: Params.kwargs) -> TReturn:
        ba = self.__context.signature.bind(*args, **kwds)
        takes : _Takes[TReturn] = self.when.takes(*args, **kwds)

        if takes.returns:
            return takes.returns

        if takes.raises:
            raise takes.raises

        if self.__context.methodname in object.__dict__:
            return object.__dict__[self.__context.methodname](ba.arguments['self'])

        raise Exception(f'Mock for method "{self.__context.methodname}({ba.arguments})" has not been set up. Try instantiating a mock with classmock = Mock.of(ClassType) and then mocking the method call with Mock.when(classmock.{self.__context.methodname}).takes({ba.arguments}).returns = returnvalue')
