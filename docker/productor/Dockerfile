FROM python:3.7-alpine

RUN mkdir -p /app
WORKDIR /app

RUN pip install kafka-python

COPY inputExample.json /app
COPY productor.py /app

CMD ["python", "/app/productor.py"]
