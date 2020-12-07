import argparse
import gzip
import json
import shutil
import time

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType(mode='rb'), help='Path to a gzip file containing the parsed topics as jsonlines')
parser.add_argument('-n', '--number', type=int, default=0, help='Report progress every NUMBER entries loaded')
parser.add_argument('-t', '--topic', action='store_true', help='Keep the topic type')
args = parser.parse_args()

print('=' * shutil.get_terminal_size()[0])
start_process_time = time.process_time()
start_time = time.perf_counter()

es = Elasticsearch()


def feed(file=args.file, topic=args.topic, progress=args.number):
    with gzip.open(file, mode='rb') as stream:
        n = 0
        for i, line in enumerate(stream, start=1):
            doc = json.loads(line)
            if not topic:
                doc['types'].remove('topic')
            yield {
                '_index': 'topics',
                '_op_type': 'create',
                '_source': doc,
            }
            n += 1
            if n == progress:
                print(i, 'entries loaded...')
                n = 0
        print(i, 'total entries loaded')


print('Removing old index...')
es.indices.delete('topics', ignore=[400, 404])

print('Creating index...')
es.indices.create(
    'topics',
    body={
        'settings': {
            'index': {
                'number_of_shards': 1,
                'number_of_replicas': 0,
            },
            'analysis': {
                'filter': {
                    'english_stop': {
                        'type': 'stop',
                        'stopwords': '_english_',
                    },
                    'english_stemmer': {
                        'type': 'stemmer',
                        'language': 'english',
                    },
                    'english_possessive_stemmer': {
                        'type': 'stemmer',
                        'language': 'possessive_english',
                    },
                    'ngram_2_3': {
                        'type': 'ngram',
                        'min_gram': 2,
                        'max_gram': 3,
                    },
                },
                'analyzer': {
                    'english_ngram': {
                        'type': 'custom',
                        'tokenizer': 'standard',
                        'filter': [
                            'english_possessive_stemmer',
                            'lowercase',
                            'asciifolding',
                            'english_stop',
                            'english_stemmer',
                            'ngram_2_3',
                        ],
                    },
                    'english_shingle': {
                        'type': 'custom',
                        'tokenizer': 'standard',
                        'filter': [
                            'english_possessive_stemmer',
                            'lowercase',
                            'asciifolding',
                            'english_stop',
                            'english_stemmer',
                            'shingle',
                        ],
                    },
                },
            },
        },
        'mappings': {
            'properties': {
                'id': {
                    'type': 'keyword',
                },
                'title': {
                    'type': 'text',
                    'analyzer': 'english_shingle',
                    'fields': {
                        'ngram': {
                            'type': 'text',
                            'analyzer': 'english_ngram',
                        },
                    },
                },
                'aliases': {
                    'type': 'text',
                    'analyzer': 'english_shingle',
                    'fields': {
                        'ngram': {
                            'type': 'text',
                            'analyzer': 'english_ngram',
                        },
                    },
                },
                'types': {
                    'type': 'keyword',
                },
            },
        },
    },
)

print('Indexing documents...')
indexed, errors = bulk(es, feed(), chunk_size=5000, raise_on_error=False, request_timeout=30)

if errors:
    with open('errors.json', mode='w', encoding='UTF-8') as out:
        json.dump(errors, out, indent=4, ensure_ascii=False)

time_elapsed = time.perf_counter() - start_time
process_time = time.process_time() - start_process_time

print('=' * shutil.get_terminal_size()[0])
print('DONE!')
print(f'Rows indexed  :  {indexed}')
print(f'Errors total  :  {len(errors)}')
print(f'Time elapsed  :  {time.strftime("%H:%M:%S", time.gmtime(time_elapsed))} ({time_elapsed} seconds)')
print(f'Process time  :  {time.strftime("%H:%M:%S", time.gmtime(process_time))} ({process_time} seconds)')
print('=' * shutil.get_terminal_size()[0])
