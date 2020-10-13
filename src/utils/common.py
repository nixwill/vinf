from typing import Set

from dataclasses import asdict, dataclass, field
from json import dumps, loads


@dataclass(eq=False)
class Data:
    title: str = None
    topic: bool = False
    types: Set[str] = field(default_factory=set)
    aliases: Set[str] = field(default_factory=set)

    def is_viable(self) -> bool:
        return self.topic

    def __add__(self, other: 'Data') -> 'Data':
        return Data(
            self.title or other.title or None,
            self.topic or other.topic,
            self.types | other.types,
            self.aliases | other.aliases,
        )

    def __iadd__(self, other: 'Data') -> 'Data':
        if not self.title:
            self.title = other.title or None
        if not self.topic:
            self.topic = other.topic
        self.types.update(other.types)
        self.aliases.update(other.aliases)
        return self

    def to_json(self, with_topic: bool = False, **kwargs) -> str:
        d = asdict(self)
        if not with_topic:
            del d['topic']
        d['types'] = tuple(d['types'])
        d['aliases'] = tuple(d['aliases'])
        return dumps(d, **kwargs)

    @classmethod
    def from_json(cls, string: str, **kwargs) -> 'Data':
        d = loads(string, **kwargs)
        if (types := d.get('types')) is not None:
            d['types'] = set(types)
        if (aliases := d.get('aliases')) is not None:
            d['aliases'] = set(aliases)
        return cls(**d)
