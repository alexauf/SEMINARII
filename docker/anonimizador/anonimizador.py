import signal
import sys
import time
import threading

import json
import hashlib

from kafka.errors import NoBrokersAvailable
from kafka import KafkaProducer
from kafka import KafkaConsumer

KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC_CONSUME = "flows"
KAFKA_TOPIC_PRODUCE = "fanonim"



def consume():
    consumer = KafkaConsumer(
        KAFKA_TOPIC_CONSUME,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest',
        group_id='event-gen')
    producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER])
    for message in consumer:

        # cargar en una estructura diccionario
        jsonvalue = json.loads(message.value)

        # anonimizar src-name
        jsonvalue["src-name"] = hashlib.sha1(jsonvalue["src-name"].encode("utf-8")).hexdigest()
        # anonimizar dst-name
        jsonvalue["dst-name"] = hashlib.sha1(jsonvalue["dst-name"].encode("utf-8")).hexdigest()

        # anonimizar src-address
        iptemp = jsonvalue["src-address"].split(".")
        jsonvalue["src-address"] = ".".join(iptemp[0:2]) + ".*"

        # anonimizar dst-address
        iptemp = jsonvalue["dst-address"].split(".")
        jsonvalue["dst-address"] = ".".join(iptemp[0:2]) + ".*"
        
        response = json.dumps(jsonvalue)

        print("CONSUMIDO:\n%s\nANONIMIZADO:\n%s\n\n" % (message.value, response), flush=True)

        producer.send(topic=KAFKA_TOPIC_PRODUCE, key=response.encode("utf-8"), value=response.encode("utf-8"))
        producer.flush()


def handler(number, frame):
    sys.exit(0)


def safe_loop(fn):
    while True:
        try:
            fn()
        except SystemExit:
            print("Good bye!")
            return
        except NoBrokersAvailable:
            time.sleep(2)
            continue
        except Exception as e:
            print(e)
            return


def main():
    signal.signal(signal.SIGTERM, handler)

    consumer = threading.Thread(target=safe_loop, args=[consume])
    consumer.start()
    consumer.join()


if __name__ == "__main__":
    main()
