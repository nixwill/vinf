import sys

from utils import parse_line_into_kv_pair


for line in sys.stdin:
    pair = parse_line_into_kv_pair(line)
    if pair is not None:
        key, value = pair
        print(key, value.to_json(with_topic=True))
