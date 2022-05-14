# SEMINARII


Para lanzar el sistema ejecutamos:
```
sudo docker-compose -f docker-compose-anonimizador.yml up -d --build
```

Una vez hecho esto el sistema completo estará corriendo. Para comprobarlo podemos ejecutar:

```
sudo docker ps
```

Podemos ver la salida que genera cada uno de los contenedores usando la instrucción logs, por ejemplo, para ver qué paquetes está escribiendo el productor en kafka hacemos:

```
sudo docker logs productor
```

Además, para algunas tareas es interesante poder acceder al contenedor, por ejemplo para ver que se está escribiendo en los topics o para escribir directamente sin necesidad de tener que generar la aplicación, para esto ejecutamos el siguiente comando:

```
sudo docker exec -it kafka /bin/bash
```

Si queremos escribir en el topic flows:

```
kafka-console-producer.sh --bootstrap-server kafka:9092 --topic flows
```

Y si queremos leer del topic fanonim:
```
kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic fanonim
```

En este caso en el que el sistema está operativo, es más sencillo ver la salida que producen las aplicaciones productor y consumidor, para ver la diferencia entre paquetes generados y anonimizados, un ejemplo puede ser el siguiente:
```
PAQUETE GENERADO:
{
    "src-name": "JOSHUA-PC-APPLE",
    "dst-name": "IDEAPAD-315",
    "ip-version": "ipv4",
    "src-address": "192.168.123.104",
    "dst-address": "172.156.72.8",
    "src-port": 58956,
    "dst-port": 63862,
    "protocol": "tcp",
    "tcp-flags": "ack",
    "first-switched": 1637147083,
    "last-switched": 1637159636,
    "bytes-in": 329616,
    "pkts-in": 278
}

PAQUETE ANONIMIZADO:
{
    "src-name": "3b1dee9700673e0fade33457a4ac2e84a9b24fc0",
    "dst-name": "8909e62f54ee4fe00e48a7f4a62dbab923ce35d7",
    "ip-version": "ipv4",
    "src-address": "192.168.*",
    "dst-address": "172.156.*",
    "src-port": 58956,
    "dst-port": 63862,
    "protocol": "tcp",
    "tcp-flags": "ack",
    "first-switched": 1637147083,
    "last-switched": 1637159636,
    "bytes-in": 329616,
    "pkts-in": 278
}
```

Por último, para terminar la ejecución del sistema:
```
sudo docker-compose -f docker-compose-anonimizador.yml down
```

