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


from goodmock import _MethodMock, Mock, Takes, When


def test_when_withvalidcontext_returnswhenfromcontext():
    # arrange
    expected_when = Mock.of(When)

    # act
    methodmock = _MethodMock('methodname', expected_when)
    actual_when = methodmock.when

    # assert
    assert expected_when == actual_when


def test_when_withnowhenincontext_raisesexception():
    # arrange
    none_when = None

    # act + assert
    with pytest.raises(Exception):
        methodmock = _MethodMock('methodname', none_when)
        methodmock.when

def test_call_withreturns_returnscorrectvalue():
    # arrange
    takes = Takes()
    expected_returns = 1
    takes.returns = expected_returns
    when_mock = Mock.of(When)
    Mock.when(when_mock.takes).takes().returns = takes

    # act
    methodmock = _MethodMock('methodmock', when_mock)
    actual_returns = methodmock()

    # assert
    assert expected_returns == actual_returns

def test_call_withraises_raisescorrectexception():
    # arrange
    takes = Takes()
    expected_raises = Exception()
    takes.raises = expected_raises
    when_mock = Mock.of(When)
    Mock.when(when_mock.takes).takes().returns = takes

    # act + assert
    with pytest.raises(Exception):
        methodmock = _MethodMock('methodmock', when_mock)
        methodmock()

def test_call_withnosetup_raisesexception():
    # arrange
    when_mock = Mock.of(When)

    # act + assert
    with pytest.raises(Exception):
        methodmock = _MethodMock('methodmock', when_mock)
        methodmock()
