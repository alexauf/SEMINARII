import signal
import sys
import time
import threading

import random
import json

from kafka.errors import NoBrokersAvailable
from kafka import KafkaProducer

KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC_PRODUCE = "flows"


names = ["PEDRO-PC", "LENOVO", "IDEAPAD-315", "ALEX-COMPUTER", "JOSHUA-PC-APPLE"]
ips = ["192.168.123.104", "192.168.154.201", "10.36.45.72", "172.156.72.8", "192.178.156.3"]
tcpflagslist = ["fin", "syn", "synack", "ack", "finsynpshack"]


def generate_packet(jsonvalue):
    srcname, dstname = random.sample(names, 2)
    srcip, dstip = random.sample(ips, 2)
    srcport, dstport = random.sample(range(49152, 65535), 2)
    first = random.randint(1637147000, 1637148000)
    last = random.randint(1637159000, 1637161000)
    bytesIn = random.randint(300000, 400000)
    pktsIn = random.randint(200, 350)
    tcp_flags = random.choice(tcpflagslist)

    jsonvalue["src-name"] = srcname
    jsonvalue["dst-name"] = dstname
    jsonvalue["src-address"] = srcip
    jsonvalue["dst-address"] = dstip
    jsonvalue["src-port"] = srcport
    jsonvalue["dst-port"] = dstport
    jsonvalue["tcp-flags"] = tcp_flags
    jsonvalue["first-switched"] = first
    jsonvalue["last-switched"] = last
    jsonvalue["bytes-in"] = bytesIn
    jsonvalue["pkts-in"] = pktsIn



def random_requests():

    inputfile = "./inputExample.json"
    with open(inputfile, "r") as f:
        filecontent = f.read()

    jsonvalue = json.loads(filecontent)

    while True:
        generate_packet(jsonvalue)
        response = json.dumps(jsonvalue)
        yield response


def produce():
    if len(sys.argv) == 2:
        delay_seconds = int(sys.argv[1])
    else:
        delay_seconds = 1
    producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER])
    for request in random_requests():
        print("PRODUCER\n%s\n\n" % (request), flush=True)
        producer.send(topic=KAFKA_TOPIC_PRODUCE, key=request.encode('utf-8'), value=request.encode('utf-8'))
        producer.flush()
        time.sleep(delay_seconds)


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

    producer = threading.Thread(target=safe_loop, args=[produce])
    producer.start()
    producer.join()


if __name__ == "__main__":
    main()
