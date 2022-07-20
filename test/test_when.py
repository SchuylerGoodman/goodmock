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

from inspect import BoundArguments, Signature
from goodmock import Mock, Takes, When


def test_takes_firsttimewithvalidarguments_createsnewtakes():
    # arrange
    boundarguments_mock = Mock.of(BoundArguments)
    boundarguments_mock.arguments = {}
    signature_mock = Mock.of(Signature)
    Mock.when(signature_mock.bind).takes().returns = boundarguments_mock

    # act
    when = When(signature_mock)
    actualtakes = when.takes()

    # assert
    assert type(actualtakes) == Takes


def test_takes_afterfirsttimewithvalidarguments_getsprevioustakes():
    # arrange
    boundarguments_mock = Mock.of(BoundArguments)
    boundarguments_mock.arguments = {}
    signature_mock = Mock.of(Signature)
    Mock.when(signature_mock.bind).takes().returns = boundarguments_mock

    # act
    when = When(signature_mock)
    actualtakes1 = when.takes()
    actualtakes2 = when.takes()

    # assert
    assert actualtakes1 == actualtakes2


def test_takes_withdifferentarguments_createdifferenttakes():
    # arrange
    boundarguments_mock1 = Mock.of(BoundArguments)
    boundarguments_mock1.arguments = {'a': 1}
    boundarguments_mock2 = Mock.of(BoundArguments)
    boundarguments_mock2.arguments = {'a': 2}
    signature_mock = Mock.of(Signature)
    Mock.when(signature_mock.bind).takes(boundarguments_mock1.arguments['a']).returns = boundarguments_mock1
    Mock.when(signature_mock.bind).takes(boundarguments_mock2.arguments['a']).returns = boundarguments_mock2

    # act
    when = When(signature_mock)
    actualtakes1 = when.takes(1)
    actualtakes2 = when.takes(2)

    # assert
    assert actualtakes1 != actualtakes2