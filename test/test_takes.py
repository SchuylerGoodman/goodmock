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


from goodmock import Takes


def test_returns_withvalidinput_setsreturns():
    # arrange
    expectedreturns = 1

    # act
    takes = Takes[int]()
    takes.returns = expectedreturns
    actualreturns = takes.returns

    # assert
    assert expectedreturns == actualreturns

def test_returns_withraisesalreadyset_raisesexception():
    # arrange
    returns = 1
    raises = Exception

    # act
    takes = Takes[int]()
    takes.returns = returns
    with pytest.raises(Exception):
        takes.raises = raises

def test_raises_withvalidinput_raisesraises():
    # arrange
    expectedraises = Exception

    # act
    takes = Takes[int]()
    takes.raises = expectedraises
    actualraises = takes.raises

    # assert
    assert expectedraises == actualraises

def test_raises_withreturnsalreadyset_raisesexception():
    # arrange
    raises = Exception
    returns = 1

    # act
    takes = Takes[int]()
    takes.raises = raises
    with pytest.raises(Exception):
        takes.returns = returns
