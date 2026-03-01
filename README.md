# 🌤️ Weather API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**API REST para gestión de dispositivos IoT, sensores y lecturas climáticas.**  
Construida con FastAPI y PostgreSQL para registrar y consultar datos meteorológicos en tiempo real.

[Ver Endpoints](#-endpoints) · [Instalación](#-instalación) · [Reportar un Bug](../../issues) · [Solicitar Feature](../../issues)

</div>

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#%EF%B8%8F-configuración)
- [Uso](#-uso)
- [Endpoints](#-endpoints)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## 📖 Descripción

**Weather API** es una API REST ligera y eficiente que permite gestionar la infraestructura de monitoreo climático: registrar dispositivos de medición, asociarles sensores y almacenar sus lecturas periódicas. Está diseñada para integrarse fácilmente con sistemas embebidos, dashboards o pipelines de análisis de datos.

---

## ✨ Características

- 📡 **Registro de dispositivos** — Alta de dispositivos IoT en la base de datos
- 🔬 **Gestión de sensores** — Asociación de sensores a dispositivos con descripción y referencia
- 📊 **Almacenamiento de lecturas** — Inserción de mediciones con marca de tiempo y valor
- 🔍 **Consulta universal** — Endpoint genérico para listar registros de cualquier tabla autorizada
- 🛡️ **Protección contra SQL Injection** — Validación de tablas permitidas en consultas dinámicas
- ⚡ **Alta performance** — Basada en FastAPI con soporte async

---

## 🛠️ Tecnologías

| Tecnología | Versión | Propósito |
|---|---|---|
| [Python](https://www.python.org/) | 3.10+ | Lenguaje base |
| [FastAPI](https://fastapi.tiangolo.com/) | 0.100+ | Framework web |
| [PostgreSQL](https://www.postgresql.org/) | 15+ | Base de datos |
| [psycopg2](https://www.psycopg.org/) | 2.9+ | Conector PostgreSQL |
| [Uvicorn](https://www.uvicorn.org/) | 0.23+ | Servidor ASGI |

---

## ✅ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- Python `>= 3.10`
- PostgreSQL `>= 15` en ejecución
- `pip` o un gestor de entornos virtuales (`venv`, `conda`)

---

## 🚀 Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/tu-usuario/weather-api.git
cd weather-api

# 2. Crea y activa un entorno virtual
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instala las dependencias
pip install fastapi psycopg2-binary uvicorn

# 4. Inicia el servidor
uvicorn main:app --reload
```

La API estará disponible en: `http://localhost:8000`  
Documentación interactiva (Swagger): `http://localhost:8000/docs`

---

## ⚙️ Configuración

Edita el bloque `DB_CONFIG` en `main.py` con tus credenciales de PostgreSQL:

```python
DB_CONFIG = {
    "host": "localhost",
    "database": "wheatherapi",
    "user": "tu_usuario",       # ⚠️ Verifica el nombre de la clave ("user", no "use")
    "password": "tu_contraseña",
    "port": 5432
}
```

> 💡 **Recomendación:** Usa variables de entorno o un archivo `.env` para no exponer credenciales en el código. Puedes usar [`python-dotenv`](https://pypi.org/project/python-dotenv/) para esto.

### Esquema de Base de Datos

Asegúrate de crear las siguientes tablas antes de usar la API:

```sql
CREATE TABLE dispositivo (
    id    INTEGER PRIMARY KEY,
    w     VARCHAR(100),
    n     VARCHAR(100)
);

CREATE TABLE sensor (
    id            INTEGER PRIMARY KEY,
    referencia    VARCHAR(100),
    descripcion   TEXT,
    dispositivo_id INTEGER REFERENCES dispositivo(id)
);

CREATE TABLE lectura (
    id         INTEGER PRIMARY KEY,
    fechahora  TIMESTAMP,
    valor      VARCHAR(50),
    sensor_id  INTEGER REFERENCES sensor(id)
);
```

---

## 📖 Uso

Una vez levantado el servidor, puedes interactuar con la API usando `curl`, [Postman](https://www.postman.com/) o directamente desde el Swagger en `/docs`.

```bash
# Verificar que la API está activa
curl http://localhost:8000/
```

---

## 📡 Endpoints

### `GET /`
Verifica el estado de la API.

**Respuesta:**
```json
{ "message": "API de Clima Funcionando" }
```

---

### `POST /insert/dispositivo`
Registra un nuevo dispositivo.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `id` | `int` | Identificador único del dispositivo |
| `w` | `str` | Código o tipo de dispositivo |
| `n` | `str` | Nombre del dispositivo |

```bash
curl -X POST "http://localhost:8000/insert/dispositivo?id=1&w=ESP32&n=Estacion-Norte"
```

---

### `POST /insert/sensor`
Registra un sensor asociado a un dispositivo.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `id` | `int` | Identificador único del sensor |
| `referencia` | `str` | Código de referencia del sensor |
| `descripcion` | `str` | Descripción del sensor |
| `disposito_id` | `int` | ID del dispositivo al que pertenece |

```bash
curl -X POST "http://localhost:8000/insert/sensor?id=1&referencia=DHT22&descripcion=Sensor+temperatura&disposito_id=1"
```

---

### `POST /insert/lectura`
Registra una lectura de un sensor.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `id` | `int` | Identificador único de la lectura |
| `fechahora` | `str` | Fecha y hora de la medición (ISO 8601 recomendado) |
| `valor` | `str` | Valor registrado por el sensor |
| `sensor_id` | `int` | ID del sensor que tomó la lectura |

```bash
curl -X POST "http://localhost:8000/insert/lectura?id=1&fechahora=2025-03-01T10:00:00&valor=23.5&sensor_id=1"
```

---

### `GET /select`
Consulta todos los registros de una tabla.

| Parámetro | Tipo | Valores permitidos |
|---|---|---|
| `table` | `str` | `dispositivo`, `sensor`, `lectura` |

```bash
curl "http://localhost:8000/select?table=lectura"
```

> ⚠️ Solo se permiten las tablas listadas para evitar inyección SQL.

---

## 📁 Estructura del Proyecto

```
weather-api/
│
├── main.py          # Aplicación principal (rutas y lógica)
├── README.md        # Documentación del proyecto
└── .gitignore       # Archivos ignorados por Git
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto:

1. Haz un **fork** del repositorio
2. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. Realiza tus cambios y haz commit: `git commit -m "feat: agrega nueva funcionalidad"`
4. Haz push a tu rama: `git push origin feature/nueva-funcionalidad`
5. Abre un **Pull Request**

Por favor, sigue el estándar de commits [Conventional Commits](https://www.conventionalcommits.org/).

---

## 📄 Licencia

Distribuido bajo la licencia **MIT**. Consulta el archivo `LICENSE` para más información.

---

<div align="center">

Hecho con ❤️ y ☕ | [⬆️ Volver arriba](#️-weather-api)

</div>
