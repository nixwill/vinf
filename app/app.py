import os

from pyspark import SparkConf, SparkContext
from utils import parse_line_into_kv_pair


conf = SparkConf().setAppName('vinf').setMaster(os.environ.get('SPARK_MASTER_URL', 'spark://localhost:7077'))
sc = SparkContext(conf=conf)

out = (
    sc
    .textFile(os.path.join(
        os.environ.get('DATA_PATH', '../data'),
        os.environ.get('SOURCE_FILE', 'freebase-head-100000000'))
    )
    .map(parse_line_into_kv_pair)
    .filter(lambda pair: pair is not None)
    .reduceByKey(lambda x, y: x + y)
    .filter(lambda pair: pair[1].is_viable())
    .mapValues(lambda val: val.to_json())
    .collect()
)

print(out)
