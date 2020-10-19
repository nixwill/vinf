FROM python:3.6-alpine
RUN apk add --no-cache bash openjdk8-jre
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
