FROM python:3.7-alpine

RUN mkdir -p /app
WORKDIR /app

RUN pip install kafka-python

COPY consumidor.py /app

CMD ["python", "/app/consumidor.py"]
