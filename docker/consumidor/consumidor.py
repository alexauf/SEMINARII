import signal
import sys
import time
import threading

import random

from kafka.errors import NoBrokersAvailable
from kafka import KafkaConsumer

KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC_CONSUME = "fanonim"



def consume():
    consumer = KafkaConsumer(
        KAFKA_TOPIC_CONSUME,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest',
        group_id='event-gen')
    for message in consumer:
        print("CONSUMER\n%s\n\n" % (message.value.decode("utf-8")), flush=True)


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
