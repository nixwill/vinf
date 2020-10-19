# VINF Project
Semestral project for VINF class

## Commands

```sh
python app/map.py < data/freebase-head-1000000 | sort -k1,1 | python app/reduce.py > data/out.jsonl
```


```sh
docker-compose up --scale spark-worker=4 spark-master spark-worker
docker-compose up pyspark-client
```
