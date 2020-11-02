FROM alpine:latest AS builder
RUN apk add --no-cache zip
COPY src /opt/app
RUN mkdir -p /opt/dist && cd /opt/app && zip -r /opt/dist/deps.zip utils && cp app.py /opt/dist/app.py

FROM bitnami/spark:3.0.1
COPY --from=builder /opt/dist .
CMD ["./bin/spark-submit", "--py-files", "deps.zip", "app.py"]
