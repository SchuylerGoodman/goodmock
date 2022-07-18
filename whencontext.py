import inspect


from dataclasses import dataclass
from goodmock.takes import _Takes
from typing import Dict


@dataclass
class _WhenContext(Dict[str, _Takes]):
    methodname: str
    signature : inspect.Signature
