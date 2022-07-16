from dataclasses import dataclass
from goodmock.setup import Setup


@dataclass
class ArgumentContext:
    setup : Setup
    calls : int
