# VINF Project
Semestral project for VINF class

## Usage

### Map Reduce using shell

```sh
python src/map.py < data/freebase-head-1000000 | sort -k1,1 | python src/reduce.py > data/out.jsonl
```

### Development cluster

#### Initial setup

```sh
mkdir out
sudo chown 1001:1001 out
```

#### Start cluster

```sh
docker-compose up --scale spark-worker=4 spark-master spark-worker
```

#### Run parse job

```sh
docker-compose build --pull spark-app
docker-compose run --rm spark-app
```
