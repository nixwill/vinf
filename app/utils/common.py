from typing import Set

from json import dumps, loads


class Data:

    def __init__(self, title: str = None, topic: bool = False, types: Set[str] = None, aliases: Set[str] = None):
        self.title = title
        self.topic = topic
        self.types = set() if types is None else types
        self.aliases = set() if aliases is None else aliases

    def is_viable(self) -> bool:
        return self.topic and self.title is not None

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
        d = self.__dict__.copy()
        if not with_topic:
            del d['topic']
        d['types'] = tuple(d['types'])
        d['aliases'] = tuple(d['aliases'])
        return dumps(d, **kwargs)

    @classmethod
    def from_json(cls, string: str, **kwargs) -> 'Data':
        d = loads(string, **kwargs)
        d['types'] = set(d['types'])
        d['aliases'] = set(d['aliases'])
        return cls(**d)
