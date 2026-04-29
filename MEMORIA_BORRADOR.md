# Trabajo de enfoque: Sistema Big Data aplicado a mantenimiento predictivo IoT

## 1. Introduccion

SmartManuTech es una empresa de manufactura avanzada que ha incorporado sensores IoT en sus lineas de produccion para monitorizar el estado de sus maquinas. Estos sensores generan datos continuamente, como temperatura, vibracion, velocidad de produccion, consumo energetico y eventos de error.

El problema principal es que, si estos datos no se procesan a tiempo, la deteccion de fallos se retrasa y el mantenimiento preventivo pierde eficacia. Para resolverlo, se ha desarrollado un prototipo funcional que procesa lecturas IoT en tiempo real, detecta anomalias, almacena historico y muestra resultados en un dashboard orientado al equipo de mantenimiento.

El objetivo del prototipo no es construir una plataforma industrial completa, sino demostrar una arquitectura Big Data aplicada, simple y escalable, que cubra el flujo completo desde la generacion de datos hasta la visualizacion de alertas.

## 2. Analisis del problema y requisitos

El flujo actual de SmartManuTech presenta tres limitaciones principales:

- Los datos de sensores se generan de forma continua, pero no se procesan con rapidez suficiente.
- La deteccion de fallos depende de revisiones posteriores o de errores ya producidos.
- El equipo de mantenimiento no dispone de una vista clara y centralizada del estado de las maquinas.

Para cubrir estas necesidades, el sistema debe:

- procesar datos IoT en tiempo real,
- almacenar lecturas historicas,
- detectar anomalias operativas,
- generar alertas de mantenimiento,
- presentar resultados de forma sencilla para el cliente final.

Las variables usadas en el prototipo son las indicadas en el enunciado: temperatura, vibracion, velocidad de produccion, consumo energetico y eventos de error. Como el enunciado no proporciona un dataset real, se ha creado un generador de datos sinteticos que simula el comportamiento de sensores industriales.

> Captura recomendada: codigo del simulador de datos IoT.

## 3. Arquitectura propuesta

La arquitectura implementada sigue un pipeline Big Data simplificado:

```text
Productor IoT Python
        -> Apache Kafka
        -> Consumidor Python
        -> SQLite + Parquet
        -> FastAPI
        -> Dashboard web
```

El productor Python simula sensores IoT y envia lecturas a Apache Kafka. Kafka actua como sistema de mensajeria para procesar flujos de datos en tiempo real. Un consumidor Python lee los mensajes, calcula el riesgo de fallo, genera alertas y almacena la informacion.

SQLite se utiliza como base de datos operativa del prototipo, mientras que Parquet se utiliza como formato analitico para historico. En un entorno industrial, esta capa podria escalarse a HDFS, AWS S3, Cassandra o Elasticsearch, segun las necesidades de volumen, consulta y disponibilidad.

> Captura recomendada: dashboard mostrando la banda de arquitectura.

## 4. Implementacion tecnica

El sistema se ha desarrollado con Python y FastAPI. La comunicacion en tiempo real se realiza con Apache Kafka mediante Docker Compose y el cliente `confluent-kafka`.

Componentes principales:

- `app/producer.py`: genera lecturas IoT y las publica en Kafka.
- `app/consumer.py`: consume lecturas desde Kafka y las procesa.
- `app/analytics.py`: calcula el riesgo y detecta anomalias.
- `app/storage.py`: gestiona SQLite y exportacion Parquet.
- `app/api.py`: expone datos mediante API REST y sirve el dashboard.
- `static/`: contiene el dashboard web.

El prototipo implementa seis tipos de alerta:

- temperatura alta,
- vibracion excesiva,
- velocidad de produccion baja,
- consumo energetico alto,
- evento de error,
- riesgo predictivo alto.

> Captura recomendada: productor enviando datos.

> Captura recomendada: consumidor procesando datos y creando alertas.

> Captura recomendada: Swagger en `/docs`.

## 5. Resultados y visualizacion

Los resultados se presentan en un dashboard web accesible desde el navegador. El panel muestra el estado de cada maquina, el riesgo calculado, metricas recientes, resumen de alertas por tipo y recomendaciones de mantenimiento.

La visualizacion esta pensada para que el equipo de mantenimiento interprete rapidamente la situacion:

- estado saludable, aviso o critico,
- puntuacion de riesgo de 0 a 100,
- tabla de alertas con mensaje y recomendacion,
- resumen de alertas por tipo,
- grafica de riesgo reciente.

Para facilitar las capturas de la entrega, se ha creado una demo controlada que genera una maquina sana y varios casos anomalos. Esta demo garantiza que aparecen los seis tipos de alerta implementados.

> Captura recomendada: dashboard tras pulsar `Demo alertas`.

> Captura recomendada: tabla de alertas con los seis codigos.

## 6. Evaluacion del sistema

El sistema cumple los criterios de evaluacion de la siguiente forma:

| Criterio | Evidencia en el proyecto |
|---|---|
| RA1 CE d: procesar datos almacenados | Las lecturas se almacenan en SQLite, se procesan y generan estado, riesgo y alertas. |
| RA1 CE e: presentar resultados faciles de interpretar | El dashboard muestra semaforos, graficas, alertas y recomendaciones claras. |
| RA4 c: generar 5 o mas alertas | Se generan seis tipos de alerta distintos. |
| RA2 CE a: justificar almacenamiento para grandes volumenes | Se usa SQLite y Parquet en el prototipo, justificando escalado a HDFS, S3, Cassandra o Elasticsearch. |

La solucion demuestra el procesamiento de datos almacenados porque cada lectura queda registrada y posteriormente se consulta para mostrar historico, estado de maquinas y alertas. Tambien permite exportar los datos a Parquet, formato habitual en entornos analiticos y data lakes.

## 7. Problemas encontrados y limitaciones

Durante el desarrollo se tomaron varias decisiones para evitar sobreingenieria. No se implemento Hadoop real porque su configuracion local anadiria complejidad sin aportar una mejora proporcional para el prototipo. En su lugar, se uso Parquet como formato analitico y se explico como podria escalarse a HDFS o S3.

Tampoco se utilizo Kafka Streams real, ya que esta tecnologia esta orientada principalmente a Java/Scala. En este prototipo se implemento procesamiento de streams sobre Kafka mediante consumidores Python, una alternativa mas adecuada al alcance del trabajo.

La principal limitacion es que los datos son sinteticos. Sin embargo, esto es razonable porque el enunciado no proporciona un dataset real y el objetivo es validar el pipeline tecnico.

## 8. Conclusion

El prototipo desarrollado permite procesar datos IoT en tiempo real, almacenar historico, detectar anomalias, generar alertas y visualizar resultados de forma clara. La arquitectura es sencilla, pero representa los componentes principales de una solucion Big Data aplicada a mantenimiento predictivo industrial.

La solucion cubre los criterios de evaluacion sin introducir complejidad innecesaria. Kafka aporta el componente de streaming real, SQLite y Parquet permiten demostrar almacenamiento y analisis historico, y FastAPI junto con el dashboard facilitan la presentacion de resultados al cliente final.

## 9. Bibliografia

Apache Kafka. (s. f.). *Apache Kafka documentation*. https://kafka.apache.org/documentation/

Confluent. (s. f.). *Confluent Kafka Python client*. https://docs.confluent.io/kafka-clients/python/current/overview.html

FastAPI. (s. f.). *FastAPI documentation*. https://fastapi.tiangolo.com/

The Apache Software Foundation. (s. f.). *Apache Parquet documentation*. https://parquet.apache.org/docs/

Python Software Foundation. (s. f.). *sqlite3: DB-API 2.0 interface for SQLite databases*. https://docs.python.org/3/library/sqlite3.html
