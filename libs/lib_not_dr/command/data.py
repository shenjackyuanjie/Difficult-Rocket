from dataclasses import dataclass, field
from typing import Set, List


class Parsed:
    ...


@dataclass
class Option:
    name: str
    shortcuts: List[str]
    optional: bool
    types: Set[type] = field(default_factory=lambda: {str})


@dataclass
class OptionGroup:
    options: List[Option]
    optional: bool = True
    exclusive: bool = False


@dataclass
class Argument:
    name: str
    types: Set[type] = field(default_factory=lambda: {str})


@dataclass
class Flag:
    name: str
    shortcuts: List[str]


@dataclass
class FlagGroup:
    flags: List[Flag]
    exclusive: bool = False

