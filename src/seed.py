import gzip
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk
from multiprocessing import cpu_count


es = Elasticsearch()


def feed(path):
    with gzip.open(path, mode='rt', encoding='utf-8') as stream:
        for line in stream:
            yield {
                '_index': 'topics',
                '_op_type': 'create',
                '_source': json.loads(line),
            }


# es.indices.delete('topics', ignore=[400, 404])

es.indices.create(
    'topics',
    body={
        'settings': {
            'analysis': {
                'analyzer': {
                    'custom_analyzer': {
                        'type': 'custom',
                        'tokenizer': 'standard',
                        'filter': ['lowercase', 'asciifolding', 'apostrophe'],
                    },
                },
            },
        },
        'mappings': {
            'properties': {
                'id': {'type': 'keyword'},
                'title': {
                    'type': 'text',
                    'analyzer': 'custom_analyzer',
                },
                'aliases': {
                    'type': 'text',
                    'analyzer': 'custom_analyzer',
                },
                'types': {'type': 'keyword'},
            },
        },
    },
)

# print(bulk(es, feed('data/out.jsonl.gz')))

for success, info in parallel_bulk(es, feed('data/out.jsonl.gz'), thread_count=cpu_count()):
    if not success:
        print('A document failed:', info)
