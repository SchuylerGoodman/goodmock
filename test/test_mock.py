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

import pytest


from goodmock import Mock


class A:
    __slots__ = ('attribute', '__weakref__')
    def method1(self, i : int) -> str: ...
    def __str__(self) -> str: ...


class B(A):
    def method2(self, i : int, s : str) -> bool: ...


class C:
    def __init__(self, a : A) -> None:
        self.__a = a

    def method(self, i : int) -> str:
        return self.__a.method1(i)


class D:
    def __init__(self) -> None:
        self.a = A()

    def method(self, i : int) -> str:
        return self.a.method1(i)


def test_mockboundmethod_withvalidparameters_returnsexpectedvalue():
    # arrange
    expected_i = 1
    expected_returns = 'return'

    # act
    a_mock = Mock.of(A)
    Mock.when(a_mock.method1).takes(expected_i).returns = expected_returns
    actual_returns = a_mock.method1(expected_i)

    # assert
    assert expected_returns == actual_returns

def test_mockboundmethod_withvalidparametersandraisesset_raisesexpectedexception():
    # arrange
    expected_i = 1
    expected_raises = Exception()

    # act
    a_mock = Mock.of(A)
    Mock.when(a_mock.method1).takes(expected_i).raises = expected_raises

    with pytest.raises(Exception):
        a_mock.method1(expected_i)

def test_mockboundmethod_withinvalidparameters_raisesexception():
    # arrange
    expected_i = 1
    unexpected_i = 2
    expected_returns = 'return'

    # act
    a_mock = Mock.of(A)
    Mock.when(a_mock.method1).takes(expected_i).returns = expected_returns

    with pytest.raises(Exception):
        a_mock.method1(unexpected_i)

def test_mockboundmethod_withoutsetup_raisesexception():
    # arrange
    expected_i = 1

    # act + assert
    a_mock = Mock.of(A)
    
    with pytest.raises(Exception):
        a_mock.method1(expected_i)

def test_mockoverloadedsystemmethod_withvalidparameters_returnsexpectedvalue():
    # arrange
    expected_returns = 'return'

    # act
    a_mock = Mock.of(A)
    Mock.when(a_mock.__str__).takes().returns = expected_returns
    actual_returns = a_mock.__str__()

    # assert
    assert expected_returns == actual_returns

def test_mockboundmethodofsuperclass_withvalidparameters_returnsexpectedvalue():
    # arrange
    expected_i = 1
    expected_returns = 'return'

    # act
    b_mock = Mock.of(B)
    Mock.when(b_mock.method1).takes(expected_i).returns = expected_returns
    actual_returns = b_mock.method1(expected_i)

    # assert
    assert expected_returns == actual_returns

def test_mockboundmethodofsubclass_withvalidparameters_returnsexpectedvalue():
    # arrange
    expected_i = 1
    expected_s = 's'
    expected_returns = 'return'

    # act
    b_mock = Mock.of(B)
    Mock.when(b_mock.method2).takes(expected_i, expected_s).returns = expected_returns
    actual_returns = b_mock.method2(expected_i, expected_s)

    # assert
    assert expected_returns == actual_returns

# Example usage
def test_classmethod_withmockdependencyinconstructor_returnsexpectedvalue():
    # arrange
    expected_i = 1
    expected_returns = 'return'
    a_mock = Mock.of(A)
    Mock.when(a_mock.method1).takes(expected_i).returns = expected_returns

    # act
    c = C(a_mock)
    actual_returns = c.method(expected_i)

    # assert
    assert expected_returns == actual_returns

def test_classmethod_withmockdependencyasattribute_returnsexpectedvalue():
    # arrange
    expected_i = 1
    expected_returns = 'return'
    a_mock = Mock.of(A)
    Mock.when(a_mock.method1).takes(expected_i).returns = expected_returns

    # act
    d = D()
    d.a = a_mock
    actual_returns = d.method(expected_i)

    # assert
    assert expected_returns == actual_returns
