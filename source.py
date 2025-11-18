from dataclasses import dataclass


@dataclass
class Source:
    name: str
    id: str
    url: str