# goodmock - A Good Mock Library for Python

This repository is for activate development of goodmock.

## _Disclaimer_
_This module makes no claims of mock magic, but it's good_

## Getting Started

All source code for this project is located in goodmock.py

### Prerequisites

goodmock relies on features introduced in [PEP 612](https://peps.python.org/pep-0612/), and only supports Python 3.10+

### Installation

_PyPi_: TODO

_Manual Installation:_ navigate to the root directory of the project and run `python -m pip install .`

### How to use goodmock

Given a class definition like:

```python
class ClassA:
    def method(int i) -> int: ...
```

You can set a return value for a class method:

```python
classa_mock = Mock.of(ClassA)
Mock.when(classa_mock.method).takes(1).returns = 2

assert classa_mock.method(1) == 2
```

Or you can set an expected exception for a class method:

```python
classa_mock = Mock.of(ClassA)
Mock.when(classa_mock.method).takes(1).raises = Exception()

with pytest.raises(Exception):
    classa_mock.method(1)
```

That's it!

## Need help?

* For more examples see the [unit tests](https://github.com/SchuylerGoodman/goodmock/test)
* File an issue via [Github Issues](https://github.com/SchuylerGoodman/goodmock/issues)

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution.