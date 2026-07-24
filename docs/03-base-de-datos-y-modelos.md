# Base De Datos Y Modelos

La capa de datos esta ubicada en `src/app/models/`. Su responsabilidad es encapsular consultas SQL, creacion de tablas y operaciones de lectura/escritura contra MariaDB.

El backend no usa SQLAlchemy como ORM. SQLAlchemy se usa solamente para manejar un pool de conexiones estable. Las consultas siguen siendo SQL directo con cursores DBAPI.

## Conexion Centralizada

Archivo: `src/app/models/db.py`.

Este archivo expone `get_conn()`, que es la funcion usada por los modelos para obtener una conexion a MariaDB.

El patron actual es:

```python
with get_conn() as con:
    cur = con.cursor()
    cur.execute("SELECT ...", (...,))
```

Ese contrato se mantiene en todos los modelos.

## SQLAlchemy Como Pool

`db.py` crea un `engine` de SQLAlchemy:

```python
engine = create_engine(
    build_database_url(),
    pool_size=...,
    max_overflow=...,
    pool_timeout=...,
    pool_recycle=...,
    pool_pre_ping=True,
    connect_args={...},
)
```

Esto permite reutilizar conexiones en vez de abrir una conexion fisica nueva para cada consulta.

La app sigue usando PyMySQL por debajo mediante la URL:

```text
mysql+pymysql://usuario:password@host:puerto/base
```

## Variables De Conexion

Las variables principales se definen en `compose.yaml`:

```yaml
- DB_HOST=mariadb
- DB_PORT=3306
- DB_NAME=playgrounds
- DB_USER=playgrounds
- DB_PASSWORD=playgrounds
```

Estas variables permiten cambiar el destino de base de datos sin modificar codigo.

## Variables Del Pool

Tambien se configuran desde `compose.yaml`:

```yaml
- DB_POOL_SIZE=5
- DB_MAX_OVERFLOW=10
- DB_POOL_TIMEOUT=30
- DB_POOL_RECYCLE=1800
- DB_CONNECT_TIMEOUT=10
- DB_READ_TIMEOUT=30
- DB_WRITE_TIMEOUT=30
```

Significado practico:

- `DB_POOL_SIZE`: cantidad base de conexiones que el pool puede mantener.
- `DB_MAX_OVERFLOW`: conexiones extra permitidas cuando hay mas carga.
- `DB_POOL_TIMEOUT`: segundos maximos esperando una conexion disponible.
- `DB_POOL_RECYCLE`: tiempo maximo de vida de una conexion antes de reciclarla.
- `DB_CONNECT_TIMEOUT`: tiempo maximo para abrir conexion con MariaDB.
- `DB_READ_TIMEOUT`: tiempo maximo esperando lectura desde MariaDB.
- `DB_WRITE_TIMEOUT`: tiempo maximo esperando escritura hacia MariaDB.

## Por Que Existe `pool_pre_ping`

`pool_pre_ping=True` hace que SQLAlchemy pruebe una conexion antes de entregarla.

Esto es importante porque MariaDB puede cerrar conexiones inactivas despues de cierto tiempo. Sin esa verificacion, la app podria intentar usar una conexion vieja y fallar.

Con `pool_pre_ping`, si la conexion ya no sirve, SQLAlchemy la descarta y abre otra.

## Wrapper De Conexion

`PooledConnection` conserva el uso actual con `with`:

```python
class PooledConnection:
    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc, tb):
        self.conn.close()
```

En este contexto, `close()` devuelve la conexion al pool. No necesariamente cierra la conexion fisica con MariaDB.

## Autocommit

La conexion se configura con:

```python
"autocommit": True
```

Esto conserva el comportamiento anterior del proyecto: cada operacion queda confirmada automaticamente sin llamar manualmente a `commit()`.

## Modelo De Articulos Administrativos

Archivo: `src/app/models/admin_db.py`.

Este modulo maneja la tabla `blog` desde el lado administrativo.

### `create_blog()`

Crea la tabla si no existe:

```sql
CREATE TABLE IF NOT EXISTS blog(
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    autor VARCHAR(150) NOT NULL,
    historia LONGTEXT NOT NULL
)
```

Si la tabla esta vacia, carga datos iniciales desde `models/blog.csv`.

### Consultas Y Operaciones

- `blogquery()`: lista articulos para administracion.
- `search_blog(val)`: busca articulos por titulo.
- `get_article(article_id)`: obtiene un articulo por ID.
- `create_article(ex, us, ma, ph)`: inserta un articulo.
- `update_article(ids, titulo, categ, aut, stor)`: actualiza un articulo.
- `delete_article(ex)`: borra articulos por lista de IDs.

## Modelo De Consultas Publicas Del Blog

Archivo: `src/app/models/queries_db.py`.

Este modulo se usa principalmente desde `home_bp.py`.

Funciones:

- `total_articulos()`: total general de articulos.
- `posts(pagina, por_pagina)`: listado paginado.
- `total_articulos_busqueda(val)`: total de resultados por busqueda.
- `buscar_posts(val, pagina, por_pagina)`: busqueda paginada por titulo.
- `read_article(article_id)`: lectura completa para vista publica.

La busqueda usa `LIKE` sobre `titulo`.

## Modelo De Usuarios

Archivo: `src/app/models/users.py`.

Este modulo maneja tabla de usuarios, login y validaciones basicas.

### `create_users()`

Crea la tabla `user` si no existe:

```sql
CREATE TABLE IF NOT EXISTS `user`(
    id INT AUTO_INCREMENT PRIMARY KEY,
    creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    fullname VARCHAR(150) NOT NULL,
    mail VARCHAR(255) NOT NULL UNIQUE,
    institution VARCHAR(150),
    charge VARCHAR(150)
)
```

Si la tabla esta vacia, crea un usuario inicial `admin` con password hasheado.

### Clase `User`

Extiende `UserMixin`, lo que permite integracion con Flask-Login.

Contiene:

- `id`
- `username`
- `password`
- `fullname`
- `mail`
- `institution`
- `charge`

### Clase `ModelUser`

Responsabilidades:

- `login(username, password)`: busca usuario y valida password.
- `get_by_id(id)`: carga usuario desde el ID guardado en sesion.

### Funciones Auxiliares

- `view_users()`: lista usuarios sin password.
- `edit_users(user_id)`: obtiene un usuario por ID.
- `user_exists(uname, mail)`: valida duplicados.
- `is_valid_email(email)`: valida formato basico de correo.
- `is_strong_password(password)`: exige longitud, mayuscula, numero y simbolo.
- `insert_user(...)`: crea usuario con password hasheado.
- `delete_user(ex)`: borra usuarios por lista de IDs.

## Modelo De Logs Tecnicos

Archivo: `src/app/models/debug_db.py`.

Este modulo maneja la tabla `request_logs`. Su objetivo es guardar informacion tecnica de requests y responses sin mezclar SQL dentro del blueprint de debug.

### `create_request_logs()`

Crea la tabla:

```sql
CREATE TABLE IF NOT EXISTS request_logs(
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    method VARCHAR(10),
    path TEXT,
    remote_addr VARCHAR(45),
    x_forwarded_for TEXT,
    x_real_ip VARCHAR(45),
    cf_connecting_ip VARCHAR(45),
    user_agent_raw TEXT,
    user_agent_platform VARCHAR(100),
    user_agent_browser VARCHAR(100),
    user_agent_version VARCHAR(100),
    ip_country_code VARCHAR(10),
    ip_country_name VARCHAR(100),
    request_headers JSON,
    request_body LONGTEXT,
    response_status INT,
    response_headers JSON,
    response_body LONGTEXT,
    duration_ms DECIMAL(10, 2)
)
```

### `insert_request_log(...)`

Inserta una fila por cada request no estatica procesada por `debug_bp.py`.

Los headers se guardan como JSON. El body se guarda como texto, serializando dicts o listas cuando aplica.

## Tablas Principales

### `blog`

Guarda articulos del blog.

Campos clave:

- `id`
- `titulo`
- `categoria`
- `autor`
- `historia`

### `user`

Guarda usuarios de la aplicacion.

Campos clave:

- `id`
- `creation`
- `username`
- `password`
- `fullname`
- `mail`
- `institution`
- `charge`

### `request_logs`

Guarda informacion tecnica para analisis y debug.

Campos clave:

- datos de ruta y metodo;
- IP y headers de proxy;
- User-Agent;
- pais cuando viene desde `CF-IPCountry`;
- headers y bodies sanitizados;
- status de response;
- duracion de la request.

## Consideraciones De Mantenimiento

- No hay migraciones formales. Los cambios de schema se hacen desde funciones `CREATE TABLE IF NOT EXISTS`.
- Si una tabla ya existe, `CREATE TABLE IF NOT EXISTS` no modifica columnas existentes.
- Si se agregan columnas nuevas a tablas ya creadas, sera necesario usar `ALTER TABLE` o recrear la base en un entorno de pruebas.
- Algunas tablas se crean al importar modulos de rutas, por ejemplo `create_blog()` y `create_users()`.
- Para crecimiento futuro convendria mover toda inicializacion de tablas a un punto unico o adoptar migraciones.
