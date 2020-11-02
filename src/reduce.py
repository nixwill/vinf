import sys

from functools import reduce
from utils import Data


previous_key, first_value_json = next(sys.stdin).split(maxsplit=1)
key_group = [Data.from_json(first_value_json)]

for line in sys.stdin:
    key, value_json = line.split(maxsplit=1)
    value = Data.from_json(value_json)

    if key == previous_key:
        key_group.append(value)
    else:
        obj = reduce(lambda x, y: x + y, key_group)
        if obj.is_viable():
            print(obj.to_json())
        previous_key = key
        key_group = [value]

if key_group:
    obj = reduce(lambda x, y: x + y, key_group)
    if obj.is_viable():
        print(obj.to_json())
