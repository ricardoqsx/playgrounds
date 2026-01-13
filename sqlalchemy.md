PROMPT PARA SEGUIR DOCUMENTANDO:
Sigue documentando en este mismo archivo, con un estilo paso a paso y lenguaje
claro para personas que saben SQL pero no SQLAlchemy. Incluye referencias
explícitas a cada archivo con su ruta exacta. Mantén el tono simple, sin jerga
innecesaria, y explica el "por qué" de cada cambio. No elimines pasos previos.

# Guia de migracion a SQLAlchemy (MariaDB)

Este documento explica, paso a paso, lo que se ha hecho hasta ahora para
integrar SQLAlchemy. Esta pensado para alguien que sabe SQL, pero no conoce
SQLAlchemy. SQLAlchemy es una capa que te permite definir tablas como clases
Python y ejecutar consultas usando una sesion, sin escribir SQL directo.

## Paso 1: Crear una unica instancia de SQLAlchemy
En lugar de crear varias conexiones, ahora existe un solo objeto `db` que
representa la conexion y el "motor" de SQLAlchemy.

Archivo: `src/app/extensions.py`
- Se creo `db = SQLAlchemy()`.
- Este `db` se importa desde otros modulos.

Por que: si tienes varias instancias de SQLAlchemy, cada una tiene su propio
metadata y sesion, y los modelos no comparten el mismo contexto.

## Paso 2: Crear configuracion centralizada de la base de datos
SQLAlchemy necesita una URI (cadena de conexion). Se centralizo en un archivo
de configuracion.

Archivo: `src/app/config.py`
- Se define `Config.SQLALCHEMY_DATABASE_URI`.
- La URI se arma desde variables de entorno:
  - `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_DATABASE`.
  - Si existe `DATABASE_URL`, se usa directamente.
- Se desactiva `SQLALCHEMY_TRACK_MODIFICATIONS`.

Archivo: `.env`
- Ya tiene `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`.
- Si tu host no es `playdb`, debes agregar `MYSQL_HOST`.

Por que: asi el mismo codigo puede apuntar a distintos entornos sin tocar el
codigo. Es lo mismo que en SQL cuando cambias el DSN.

## Paso 3: Inicializar SQLAlchemy en la app Flask
Ahora la aplicacion carga la configuracion y conecta SQLAlchemy en un solo lugar.

Archivo: `src/app/__init__.py`
- Se importa `Config` y `db`.
- Se llama `app.config.from_object(Config)`.
- Se llama `db.init_app(app)`.

Por que: esta inicializacion se hace una sola vez al crear la app, igual que
cuando registras un pool de conexiones en una app web.

## Paso 4: Usar el `db` compartido en los modelos SQLAlchemy
Los modelos SQLAlchemy deben usar el `db` central, no crear uno nuevo.

Archivo: `src/app/models/admin_mdb.py`
- Se elimino `db = SQLAlchemy()` local.
- Ahora se importa `db` desde `src/app/extensions.py`.
- El modelo `Blog` sigue siendo una tabla llamada `blog`.

Archivo: `src/app/models/queries_mdb.py`
- Se elimino `db = SQLAlchemy()` local.
- Ahora se importa `db` desde `src/app/extensions.py`.

Por que: asi todos los modelos y consultas usan la misma sesion.

## Paso 5: Crear tablas y cargar datos iniciales
La funcion que crea la tabla y carga el CSV esta en el modelo de MariaDB.

Archivo: `src/app/models/admin_mdb.py`
- `create_blog()` ejecuta `db.create_all()` para crear la tabla.
- Si la tabla esta vacia, carga datos desde `blog.csv`.

Nota: esto es equivalente a ejecutar `CREATE TABLE` y luego `INSERT`.

## Estado actual de la migracion
SQLAlchemy ya esta configurado y listo, pero la app aun usa SQLite en algunas
rutas.

Archivos que siguen usando SQLite:
- `src/app/models/admin_db.py`
- `src/app/models/queries_db.py`
- `src/app/routes/admin_bp.py` importa `admin_db`.
- `src/app/routes/home_bp.py` importa `queries_db`.

Para terminar la migracion, esas rutas deben cambiarse para usar consultas
hechas con SQLAlchemy y el modelo `Blog` (MariaDB).
