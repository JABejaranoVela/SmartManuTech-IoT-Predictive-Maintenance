# AGENTS.md

## Reglas De Trabajo En Este Proyecto

- Antes de modificar cualquier archivo del proyecto, explicar:
  - que se va a hacer,
  - como se va a hacer,
  - para que sirve,
  - que archivos se tocaran.
- Esperar permiso explicito del usuario antes de hacer cambios.
- No borrar datos, base de datos, entorno virtual, contenedores Docker ni archivos generados sin permiso.
- Priorizar una solucion simple que cubra la rubrica del PDF sin sobreingenieria.
- Mantener Kafka como componente Big Data real del prototipo.
- Mantener Hadoop, Cassandra y Elasticsearch solo como escalados teoricos salvo permiso explicito.
- Usar nombres claros y capturas faciles de defender en la memoria.

## Base Tecnica Actual

- Backend/API: FastAPI.
- Streaming: Apache Kafka levantado con Docker Compose.
- Productor IoT: Python con `confluent-kafka`.
- Consumidor stream: Python con `confluent-kafka`.
- Procesamiento: reglas Python de anomalias y score de riesgo.
- Almacenamiento operativo: SQLite.
- Dashboard: HTML, CSS y JavaScript servido por FastAPI.

## Comandos Habituales

Ejecutar siempre desde la carpeta del proyecto:

```powershell
cd "D:\Curso_BigData_IA\Big Data Aplicado\TrabajoEnfoque\superfresh-demand-forecasting"
```

Levantar Kafka:

```powershell
docker compose up -d
```

Ejecutar API sin activar el entorno:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.api:app --reload
```

Ejecutar consumidor:

```powershell
.\.venv\Scripts\python.exe -m app.consumer
```

Ejecutar productor:

```powershell
.\.venv\Scripts\python.exe -m app.producer
```

## Nota Sobre El Entorno Virtual

El entorno `.venv` existe y tiene dependencias instaladas, pero en la inspeccion inicial faltaban los scripts de activacion de PowerShell. Por eso puede funcionar:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.api:app --reload
```

aunque falle:

```powershell
.\.venv\Scripts\Activate.ps1
```

No regenerar el entorno sin permiso, porque puede afectar a dependencias instaladas.
