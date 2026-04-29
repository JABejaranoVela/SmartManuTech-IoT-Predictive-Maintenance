# SmartManuTech IoT Predictive Maintenance

Prototipo Big Data aplicado para procesar datos IoT industriales en tiempo real con Apache Kafka, detectar anomalias, almacenar historico y mostrar resultados en un dashboard.

## Arquitectura

```text
Productor IoT Python
        -> Apache Kafka
        -> Consumidor Python
        -> SQLite
        -> FastAPI
        -> Dashboard web
```

## Puesta en marcha

Ejecutar siempre desde la carpeta del proyecto:

```powershell
cd "D:\Curso_BigData_IA\Big Data Aplicado\TrabajoEnfoque\superfresh-demand-forecasting"
```

1. Activar entorno e instalar dependencias si hiciera falta:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Si PowerShell bloquea la activacion:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Tambien se puede ejecutar todo sin activar el entorno:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.api:app --reload
```

2. Levantar Kafka:

```powershell
docker compose up -d
```

3. Lanzar el consumidor:

```powershell
.\.venv\Scripts\python.exe -m app.consumer
```

4. En otra terminal, lanzar el productor IoT:

```powershell
.\.venv\Scripts\python.exe -m app.producer
```

5. En otra terminal, lanzar la API y el dashboard:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.api:app --reload
```

Abrir:

```text
http://127.0.0.1:8000
```

## Demo recomendada para capturas

Para preparar una captura clara del dashboard:

1. Levantar la API.
2. Abrir `http://127.0.0.1:8000`.
3. Pulsar el boton `Demo alertas`.

Ese boton genera casos controlados:

- maquina sana,
- temperatura alta,
- vibracion alta,
- velocidad baja,
- consumo energetico alto,
- error critico,
- riesgo predictivo alto.

Tambien se puede lanzar por API:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8000/api/demo
```

## Endpoints utiles

- `GET /`: dashboard.
- `GET /docs`: Swagger de FastAPI.
- `GET /api/machines`: estado agregado por maquina.
- `GET /api/readings`: ultimas lecturas.
- `GET /api/alerts`: alertas generadas.
- `POST /api/simulate`: genera y procesa una lectura sin pasar por Kafka, util para demo rapida.
- `POST /api/demo`: genera una demo controlada con todos los tipos de alerta.
- `POST /api/reset-demo`: limpia lecturas/alertas y genera demo controlada.

## Alertas implementadas

- `TEMP_HIGH`: temperatura alta.
- `VIBRATION_HIGH`: vibracion excesiva.
- `SPEED_LOW`: velocidad de produccion baja.
- `ENERGY_HIGH`: consumo energetico alto.
- `ERROR_EVENT`: error critico.
- `PREDICTIVE_RISK_HIGH`: riesgo predictivo alto.

## Relacion con criterios de evaluacion

| Criterio | Como se demuestra |
|---|---|
| RA1 CE d: procesar datos almacenados | Las lecturas se guardan en SQLite, se procesan y generan estado, riesgo y alertas. |
| RA1 CE e: resultados faciles de interpretar | El dashboard muestra semaforos, riesgo, graficas, alertas y recomendaciones. |
| RA4 c: 5 o mas alertas | La demo controlada genera 6 tipos de alerta distintos. |
| RA2 CE a: importancia del almacenamiento | Se usa SQLite como almacenamiento operativo del prototipo; se justifica escalado a S3, HDFS, Cassandra o Elasticsearch. |

## Capturas recomendadas para el PDF

- Docker/Kafka levantado con `docker compose up -d`.
- Productor enviando lecturas con `python -m app.producer`.
- Consumidor procesando Kafka con `python -m app.consumer`.
- Swagger en `http://127.0.0.1:8000/docs`.
- Dashboard despues de pulsar `Demo alertas`.
- Tabla de alertas mostrando los 6 codigos.

## Base de datos

SQLite:

```text
data/smartmanutech.db
```

Tablas:

- `readings`: lecturas IoT procesadas.
- `alerts`: alertas generadas.

## Nota para la memoria

El prototipo usa consumidores Python para procesar streams sobre Kafka. En un entorno empresarial Java/Scala, esta capa podria implementarse con Kafka Streams. SQLite se usa como almacenamiento operativo local; en produccion el historico podria migrarse a S3, HDFS, Cassandra o Elasticsearch.

Los datos del prototipo son sinteticos. Se generan localmente porque el enunciado no proporciona un dataset real de SmartManuTech. Las variables simuladas reproducen las indicadas en el PDF: temperatura, vibracion, velocidad de produccion, consumo energetico y eventos de error.

## Comandos rapidos de verificacion

Ver numero de registros en SQLite:

```powershell
.\.venv\Scripts\python.exe -c "import sqlite3; c=sqlite3.connect('data/smartmanutech.db'); print(c.execute('select count(*) from readings').fetchone()); print(c.execute('select count(*) from alerts').fetchone())"
```

Crear demo controlada desde terminal:

```powershell
.\.venv\Scripts\python.exe -m app.demo_seed
```

Crear demo limpia para capturas:

```powershell
.\.venv\Scripts\python.exe -m app.reset_demo
```
