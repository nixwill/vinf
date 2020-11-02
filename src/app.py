import argparse
import os

from pyspark import SparkConf, SparkContext
from utils import parse_line_into_kv_pair


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', default=os.environ.get('APP_NAME', 'VINF'), help='Spark application name')
parser.add_argument('-m', '--master', default=os.environ.get('SPARK_MASTER_URL', 'spark://localhost:7077'))
parser.add_argument('-i', '--input', default=os.environ.get('INPUT_FILE', 'freebase-rdf-latest.gz'), help='input file to parse')
parser.add_argument('-o', '--output', default=os.environ.get('OUTPUT_DIR', 'out'), help='output directory')
parser.add_argument('-c', '--compress', action='store_const', const='org.apache.hadoop.io.compress.GzipCodec', default=os.environ.get('OUTPUT_COMPRESSION'), help='compress with gzip')
parser.add_argument('--collect', action='store_true', help='collect and print result')
args = parser.parse_args()
print('ARGS:', args)


conf = SparkConf().setAppName(args.name).setMaster(args.master)
sc = SparkContext(conf=conf)

rdd = (
    sc
    .textFile(args.input)
    .map(parse_line_into_kv_pair)
    .filter(lambda pair: pair is not None)
    .reduceByKey(lambda x, y: x + y)
    .filter(lambda pair: pair[1].is_viable())
    .map(lambda pair: pair[1].to_json())
)

if args.collect:
    print(*rdd.collect(), sep='\n')
else:
    rdd.saveAsTextFile(args.output, args.compress)
