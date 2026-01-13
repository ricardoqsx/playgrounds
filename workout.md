# Migracion SQLite -> MariaDB (Revision)

## Enfoque rapido
- La app hoy usa `sqlite3` directo en `src/app/models/*.py` con SQL crudo.
- Para MariaDB con SQLAlchemy hay cambios moderados, pero viables: crear modelos ORM, usar `engine`/`session`, y reemplazar `sqlite3`.
- En rutas y templates no se ve acoplamiento a SQLite; la dependencia esta concentrada en `models`.

## 1) Docker: dependencias/cambios necesarios
**Actual:** `Dockerfile` usa `python:alpine` y solo instala `requirements.txt`.

**Para MariaDB + SQLAlchemy (opciones):**
1) **Driver puro Python (recomendado por simplicidad)**
   - Paquetes: `SQLAlchemy`, `PyMySQL`.
   - Ventaja: sin dependencias del sistema.
   - Docker: no necesitas `mariadb-dev` ni `gcc`.

2) **Driver nativo (mysqlclient)**
   - Paquetes: `SQLAlchemy`, `mysqlclient`.
   - Requiere libs del sistema y compilador.
   - En Alpine necesitaras `mariadb-connector-c-dev` o `mariadb-dev`, `gcc`, `musl-dev`, `python3-dev`.

**Notas Docker adicionales:**
- En `compose.yaml` faltaria agregar un servicio `mariadb` (si vas a correrlo localmente) y variables `DB_HOST`, `DB_USER`, etc.
- Si quieres evitar dolores de compilacion, considera cambiar a `python:3.12-slim` o usar `PyMySQL` en Alpine.

## 2) Scripts SQL en `src/app/models`: dificultad de migracion
**Archivos:**
- `src/app/models/admin_db.py`
- `src/app/models/queries_db.py`
- `src/app/models/users.py`

**Observaciones clave:**
- Todas las consultas son SQLite directo con `sqlite3` y parametros `?`.
- Hay SQL especifico de SQLite:
  - `autoincrement` en `CREATE TABLE`.
  - `datetime('now', 'localtime')`.
  - `substr(historia, 1, 300) || '...'` (concatenacion `||`).
- Se crean dos BD separadas: `blog.db` y `user.db` (dos conexiones distintas).
- Carga inicial via `pandas.to_sql` con CSV.

**Impacto para MariaDB con SQLAlchemy:**
- **Reescritura necesaria**: los `sqlite3.connect` deben reemplazarse por `SQLAlchemy engine + Session`.
- **SQL puntual** se puede migrar a ORM o SQLAlchemy Core.
- **Cambios no complejos**: CRUD simple, pocos joins, sin triggers.
- **Partes a cuidar**:
  - Conversion de `datetime('now', 'localtime')` a `CURRENT_TIMESTAMP` en MariaDB.
  - `substr`/`concat`: en MariaDB es `SUBSTRING` y `CONCAT`.
  - `autoincrement` pasa a `AUTO_INCREMENT`.
  - `pandas.to_sql` con MariaDB requiere `SQLAlchemy` + driver (`pymysql`/`mysqlclient`).

**Evaluacion de esfuerzo:**
- **No necesitas iniciar de cero**. La migracion es lineal, pero requiere crear modelos ORM y reescribir funciones.
- **Tiempo estimado**: bajo-medio (1-3 dias) segun nivel de pruebas/ajustes.

## 3) Rutas / static / templates
- **Correcto:** la mayor parte de `routes` solo consume funciones de `models` y no tiene SQL.
- **Riesgo minimo**: si mantienes la misma firma de funciones (inputs/outputs), no deberia cambiar nada en rutas.
- **Nota**: si cambias el tipo de retorno (por ejemplo, ORM objects en vez de tuplas), hay que adaptar las rutas/templates.

## Migracion gradual con 2 opciones activas (SQLite + MariaDB)
Si, se puede migrar por etapas manteniendo ambas bases activas mientras ajustas el codigo. Recomendaciones:
- **Capa de acceso unica**: define un solo modulo de conexion que pueda apuntar a SQLite o MariaDB segun config/env (por ejemplo `DB_BACKEND=sqlite|mariadb`).
- **Mantener firmas**: conserva las funciones publicas actuales para que `routes` no cambie mientras mueves la implementacion por debajo.
- **Transicion por modulo**: migra primero `users` o `blog` (uno a la vez) y deja el otro en SQLite hasta cerrar pruebas.
- **Sincronizacion temporal**: si necesitas datos en ambos, agrega una rutina de migracion puntual (export/import) o escribe dualmente solo durante una ventana corta.
- **Datos semilla**: separa `seed` para que puedas cargar CSV en MariaDB sin tocar SQLite.
- **Pruebas mixtas**: habilita un entorno de testing para cada backend y valida login + CRUD + busqueda en ambos.

## Plan de trabajo sugerido
1) Definir estrategia de driver: `PyMySQL` (simple) o `mysqlclient` (nativo).
2) Crear `config` para conexion MariaDB (host, user, pass, db, port).
3) Crear modelos ORM equivalentes a `blog` y `user`.
4) Reescribir funciones de `admin_db.py`, `queries_db.py`, `users.py` usando SQLAlchemy.
5) Ajustar helpers de inicializacion (seed desde CSV + usuario admin).
6) Probar endpoints clave: login, listar/crear/editar/borrar articulos, buscar.
7) Ajustar Docker/compose: agregar servicio MariaDB o variables de conexion.

## Plan de trabajo paralelo (propuesta)
**Pilar A - Infra / dependencias**
1) Agregar dependencias en `Dockerfile`, `src/requirements.txt` y `compose.yaml`.
2) Definir variables de entorno para MariaDB (host, user, pass, db, port).
3) (Opcional) Agregar servicio MariaDB en `compose.yaml` para entorno local.

**Pilar B - Nuevo modulo SQLAlchemy**
1) Crear `src/app/models/queries_mdb.py` con SQLAlchemy.
2) Implementar funciones con los mismos nombres que `src/app/models/queries_db.py`.
3) Mantener el mismo formato de retorno (tuplas/listas) para no tocar rutas.

**Pilar C - Migracion gradual**
1) Activar switch por config/env para elegir backend (SQLite vs MariaDB).
2) Migrar por modulo (primero `queries_mdb.py`, luego `users`/`admin` si aplica).
3) Validar endpoints clave en ambos backends antes de cambiar imports.

**Entregable diario sugerido**
1) Dia 1: dependencias + conexion MariaDB + stub de `queries_mdb.py`.
2) Dia 2: CRUD y busquedas en `queries_mdb.py` con mismos retornos.
3) Dia 3: pruebas y ajuste final de rutas/imports.

## Recomendacion final
- Migrar por etapas es viable: primero mover `users` y `blog` a SQLAlchemy manteniendo firmas.
- No es necesario reescribir rutas ni templates si preservas el formato de retorno.
- La carga inicial con CSV se mantiene con `pandas` + SQLAlchemy.
