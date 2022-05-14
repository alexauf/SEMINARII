FROM python:3.7-alpine

RUN mkdir -p /app
WORKDIR /app

RUN pip install kafka-python

COPY anonimizador.py /app

CMD ["python", "/app/anonimizador.py"]
