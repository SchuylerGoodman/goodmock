"""
Copyright 2022 Schuyler Goodman

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


"""A good mock library for python.

Provides simple functionality for mocking python classes.

    Typical usage example:

    Given a class definition like:
        class ClassA:
            def method(int i) -> int: ...

    You can,
        set a return value for a class method:

            classa_mock = Mock.of(ClassA)
            Mock.when(classa_mock.method).takes(1).returns = 2

            assert classa_mock.method(1) == 2

        set an expected exception for a class method:

            classa_mock = Mock.of(ClassA)
            Mock.when(classa_mock.method).takes(1).raises = Exception()

            with pytest.raises(Exception):
                classa_mock.method(1)
"""


import inspect


from types import new_class
from typing import Callable, Dict, Generic, ParamSpec, Type, TypeVar


TMock = TypeVar('TMock')
Params = ParamSpec('Params')
TReturn = TypeVar('TReturn')


class Takes(Generic[TReturn]):
    """A Takes object for specifying an expected return value or exception

    Every mocked method will map to a Takes instance for every set of parameter value combinations
    """
    def __init__(self):
        """Constructs a Takes instance
        """
        self.__returns : TReturn = None
        self.__raises : Exception = None

    @property
    def returns(self) -> TReturn:
        """Get the expected return value

        Returns:
            The expected return value
        """
        return self.__returns

    @returns.setter
    def returns(self, value : TReturn) -> None:
        """Sets the expected return value

        Typical usage example:
            class ClassA:
                def method(int i) -> int: ...

            classa_mock = Mock.of(ClassA)
            Mock.when(classa_mock.method).takes(1).returns = 2

            assert classa_mock.method(1) == 2

        Args:
            value: A value of type TReturn

        Raises:
            Exception:
                An expected return value and error cannot both be set for the same parameters
        """
        if self.raises is not None:
            raise Exception('Mock cannot both return a value and raise an exception')

        self.__returns = value

    @property
    def raises(self) -> Exception:
        """Get the expected exception

        Returns:
            The expected exception
        """
        return self.__raises

    @raises.setter
    def raises(self, value : Exception) -> None:
        """Sets the expected exception

        Typical usage example:
            class ClassA:
                def method(int i) -> int: ...

            classa_mock = Mock.of(ClassA)
            Mock.when(classa_mock.method).takes(1).raises = Exception()

            with pytest.raises(Exception):
                classa_mock.method(1)

        Args:
            value: An exception

        Raises:
            Exception:
                An expected return value and error cannot both be set for the same parameters
        """
        if self.returns is not None:
            raise Exception('Mock cannot both return a value and raise an exception')

        self.__raises = value


class When(Generic[Params, TReturn]):
    """A When object represents the mapping from parameter values to Takes objects.

    Every mocked method has a unique When instance. It can be used to retrieve Takes objects
    specific to the given parameter values that enables the definition of return values or
    expected errors for the method.
    """
    def __init__(self, signature : inspect.Signature) -> None:
        """Constructs a When instance from the given _WhenContext object.

        This method should not be called directly. Use Mock.when instead.

        Args:
            signature:
                The signature of the method represented by this When instance
        """
        self.__context : Dict[str, Takes] = {}
        self.__signature = signature

    def takes(self, *args : Params.args, **kwargs : Params.kwargs) -> Takes[TReturn]:
        """Maps the given arguments to a Takes object

        Typical usage example:
            class ClassA:
                def method(int i) -> int: ...

            classa_mock = Mock.of(ClassA)
            Mock.when(classa_mock.method).takes(1).returns = 2

            assert classa_mock.method(1) == 2

        Args:
            *args:
                The positional arguments to bind to the method represented by this When instance
            **kwargs:
                The keyword arguments to bind to the method represented by this When instance

        Returns:
            The Takes object specific to the given parameter values that enables the definition
            of return values or expected errors for the method.
        """
        argstr = self._hasharguments(True, *args, **kwargs)

        if argstr not in self.__context:
            self.__context[argstr] = Takes()

        return self.__context[argstr]

    def _hasharguments(self, omitself : bool, *args : Params.args, **kwargs : Params.kwargs) -> str:
        """Hash the given arguments to a string

        Takes positional and keyword arguments and binds them to the signature of the method
        represented by this When instance, then returns them as a string

        Args:
            omitself:
                A bool that represents whether the returned hash should include the 'self' parameter,
                if it was passed in
            *args:
                The positional arguments to bind to the method represented by this When instance
            **kwargs:
                The keyword arguments to bind to the method represented by this When instance

        Returns:
            A string hash of the arguments, in the form "key1name=key1value,...,keynname=keynvalue"
        """
        ba = self.__signature.bind(*args, **kwargs)

        keys = []
        for (key, value) in ba.arguments.items():
            if omitself and key == 'self':
                continue

            keys.append(f'{key}={value}')

        hash = ','.join(keys)

        return hash


class _MethodMock(Generic[Params, TReturn], Callable[Params, TReturn]):
    """A _MethodMock object replaces each method on the mock instance.

    _MethodMock overloads the __call__ method, which allows it to intercept the target arguments
    and get the matching Takes instance.
    """
    def __init__(self, methodname : str, when : When[Params, TReturn]) -> None:
        """Constructs a _MethodMock instance from the methodname and the When instance
        representing the method.

        Args:
            methodname: The name of the method mocked by this _MethodMock instance
            when: The When instance representing the mocked method
        """
        self.__methodname = methodname
        self.__when = when

    @property
    def when(self) -> When[Params, TReturn]:
        """Gets the When object representing the mocked method
        
        Returns:
            The When object representing the mocked method

        Raises:
            Exception: An unknown error occurred while initializing the mock object
        """
        if not self.__when:
            raise Exception(f'There was an issue initializing the mock') # TODO more useful message

        return self.__when

    def __call__(self, *args: Params.args, **kwds: Params.kwargs) -> TReturn:
        """Replaces the behavior of invocation of the target method with the mock behavior

        Returns:
            If Mock.when(mock.method).takes(...).returns has been set,
            it will return the expected value.

        Raises:
            ?:
                If Mock.when(mock.method).takes(...).raises has been set,
                it will raise the expected error.
            Exception: 
                If neither Mock.when(mock.method).takes(...).returns nor
                Mock.when(mock.method).takes(...).raises has been set
        """
        takes : Takes[TReturn] = self.when.takes(*args, **kwds)

        if takes.returns:
            return takes.returns

        if takes.raises:
            raise takes.raises

        argstr = self.when._hasharguments(True, *args, **kwds)
        raise Exception(f'Mock for method "{self.__methodname}({argstr})" has not been set up. Try instantiating a mock with classmock = Mock.of(ClassType) and then mocking the method call with Mock.when(classmock.{self.__methodname}).takes({argstr}).returns = returnvalue')

class Mock:
    """Static class entry point for mocking python classes.
    """
    @staticmethod
    def of(mockedtype : Type[TMock]) -> TMock:
        """Returns a mock instance of the given class type

        The mock instance can be used as the class itself would, but all methods
        and attributes must be set up first with Mock.when(mock.method)
        
        Args:
            mockedtype: The class type to mock

        Returns:
            A mock instance with the methods and attributes of the given class type
        """
        mockedmembers = {}
        slots = []
        for membername, member in inspect.getmembers(mockedtype):
            if (inspect.isfunction(member)):
                if membername == '__init__':
                    member = Mock.__makenoopmock(member)
                else:
                    member = Mock.__makemockedmethod(member)
            elif membername == '__slots__':
                slots = member
                continue

            mockedmembers[membername] = member

        mocktype : mockedtype = new_class(
            f'mock_{mockedtype.__name__}',
            (mockedtype, ),
            exec_body=lambda ns : ns.update(mockedmembers))

        mock : mockedtype = object.__new__(mocktype)

        for slot in slots:
            if slot != '__weakref__':
                setattr(mock, slot, None)

        return mock

    @staticmethod
    def when(method : _MethodMock[Params, TReturn]) -> When[Params, TReturn]:
        """Gets the When instance associated with the given method.
        
        The When object can be used to specify the expected result of calling the method
        with specific parameter values.

        Args:
            method: The method for which to set up the expected result.

        Returns:
            The When instance associated with the given method.

        Raises:
            Exception: The input method was not associated with a mock instance.
        """
        if not isinstance(method, _MethodMock):
            raise Exception(f'Input method must be bound to a mock instance. Try instantiating a mock with classmock = Mock.of(ClassType) and then mocking a method call with Mock.when(classmock.{method.__name__}).')

        return method.when

    @staticmethod
    def __makenoopmock(method : Callable[Params, TReturn]) -> Callable[Params, TReturn]:
        """Make a No Operation method that raises an exception when called.
        
        This should be used to mock methods that should not be called on the mock object, like __init__
        
        Args:
            method: The method that should not be called

        Raises:
            Exception: This method should not be called by tests
        """
        def noopmock(*args : Params.args, **kwargs : Params.kwargs) -> TReturn:
            raise Exception(f'Cannot call method {method.__name__} on mock')

        return noopmock

    @staticmethod
    def __makemockedmethod(method : Callable[Params, TReturn]) -> Callable[Params, TReturn]:
        """Create the mock method based on the given method

        Args:
            method: The method to mock

        Returns:
            The callable method with parameters that match the given method with which
            expected results can be specified
        """
        methodname = method.__name__
        signature = inspect.signature(method)
        parameterswithoutself = [ param for param in signature.parameters.values() if param.name != 'self' ]
        signature = signature.replace(parameters=parameterswithoutself)
        when = When(signature)

        return _MethodMock(methodname, when)
