# PLANS.md

## Objetivo Del Proyecto

Construir un prototipo funcional para SmartManuTech que procese datos IoT industriales, detecte anomalias, almacene historico y presente resultados claros para mantenimiento predictivo.

La prioridad es cubrir la rubrica del PDF con una app simple, demostrable y facil de explicar.

## Arquitectura Aprobada

```text
Productor IoT Python
        -> Apache Kafka
        -> Consumidor Python
        -> SQLite + Parquet
        -> FastAPI
        -> Dashboard web
```

## Cobertura De Criterios De Evaluacion

- RA1 CE d: procesar datos almacenados.
  - Las lecturas se guardan en SQLite.
  - El sistema calcula estado, riesgo y alertas.
  - El historico se puede exportar a Parquet.

- RA1 CE e: presentar resultados faciles de interpretar.
  - Dashboard con estado de maquinas, riesgo, graficas y tabla de alertas.
  - API documentada automaticamente en Swagger.

- RA4 c: generar 5 o mas alertas.
  - `TEMP_HIGH`: temperatura alta.
  - `VIBRATION_HIGH`: vibracion excesiva.
  - `SPEED_LOW`: baja velocidad de produccion.
  - `ENERGY_HIGH`: consumo energetico anomalo.
  - `ERROR_EVENT`: evento de error.
  - `PREDICTIVE_RISK_HIGH`: riesgo predictivo alto.

- RA2 CE a: justificar almacenamiento Big Data.
  - SQLite se usa como almacenamiento operativo local.
  - Parquet se usa como formato analitico.
  - En memoria se justifica que en produccion se podria escalar a S3, HDFS, Cassandra o Elasticsearch.

## Decisiones Tecnicas

- Usar Kafka real mediante Docker Compose.
- Usar `confluent-kafka` en Python porque es compatible con Python 3.13 en Windows.
- No usar Kafka Streams real porque esta orientado a Java/Scala.
- Redaccion recomendada para la memoria:
  - "El prototipo implementa procesamiento de streams sobre Apache Kafka mediante consumidores Python. En un entorno empresarial Java, esta capa podria implementarse con Kafka Streams."
- No implementar Hadoop real para evitar complejidad innecesaria.
- No implementar Cassandra ni Elasticsearch salvo que se decida ampliar el alcance.

## Base De Datos Actual

Archivo SQLite:

```text
data/smartmanutech.db
```

Archivo Parquet:

```text
data/readings.parquet
```

Tablas:

- `readings`: lecturas IoT procesadas.
- `alerts`: alertas generadas.

Campos principales de `readings`:

- `timestamp`
- `machine_id`
- `temperature_c`
- `vibration_mm_s`
- `production_speed_pct`
- `energy_kw`
- `error_code`
- `risk_score`
- `status`

Campos principales de `alerts`:

- `timestamp`
- `machine_id`
- `code`
- `severity`
- `message`
- `recommendation`
- `reading_id`

## Evidencias Recomendadas Para La Memoria

- Captura de Docker con Kafka levantado.
- Captura del productor generando lecturas.
- Captura del consumidor procesando mensajes.
- Captura de Swagger en `/docs`.
- Captura del dashboard en `/`.
- Captura de la tabla de alertas con 5 o mas tipos.
- Captura o explicacion de SQLite y Parquet como almacenamiento.

## Siguientes Mejoras Posibles

- Regenerar correctamente el entorno virtual para recuperar `Activate.ps1`.
- Anadir un script `scripts/demo_seed.py` para generar datos de demo controlados.
- Anadir una pagina de documentacion corta dentro del dashboard con la arquitectura.
- Preparar capturas y texto final para la memoria.
