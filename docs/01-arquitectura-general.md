# Arquitectura General

Este proyecto es una aplicacion web hecha con Flask. Su objetivo principal es servir como playground para probar una estructura modular de backend, templates, estilos, autenticacion, administracion de articulos y gestion de usuarios.

La app esta pensada como una base sencilla pero extensible. No usa un framework grande ni una arquitectura compleja; separa responsabilidades en rutas, modelos, templates y archivos estaticos.

## Stack Principal

- Python con Flask como framework web.
- Jinja2 para renderizar HTML desde templates.
- MariaDB como base de datos principal.
- PyMySQL como driver de conexion hacia MariaDB.
- SQLAlchemy usado solo para pooling de conexiones, no como ORM.
- Flask-Login para manejar sesiones de usuario.
- Flask-WTF con CSRFProtect para proteccion CSRF.
- Bootstrap local para estilos base y componentes.
- CSS propio para apariencia, temas y ajustes visuales.
- Docker Compose para levantar la app y la base de datos.

## Estructura Principal

La aplicacion vive dentro de `src/`:

```text
src/
├── run.py
└── app/
    ├── __init__.py
    ├── models/
    ├── routes/
    ├── static/
    └── templates/
```

La raiz del proyecto contiene archivos de operacion:

```text
compose.yaml
Dockerfile
README.md
restart.sh
```

## Flujo De Arranque

El contenedor ejecuta `python3 run.py` desde el `Dockerfile`.

`src/run.py` crea la aplicacion con:

```python
app = create_app()
```

Luego inicia Flask en modo debug:

```python
app.run(host='0.0.0.0', port='8050', debug=True)
```

La funcion `create_app()` esta en `src/app/__init__.py`. Ahi se configura:

- La instancia principal de Flask.
- Flask-Login.
- CSRFProtect.
- La clave secreta de Flask.
- La tabla de logs tecnicos de requests.
- Los blueprints de la aplicacion.
- Los handlers de error 401 y 404.

## Blueprints Registrados

Los blueprints estan en `src/app/routes/` y se registran en `create_app()`:

- `auth`: login, registro y logout.
- `admin`: administracion de articulos.
- `home`: vista publica del blog.
- `pruebas`: ruta simple de pruebas.
- `debug_bp`: logging tecnico de requests y responses.
- `users`: administracion de usuarios.

Cada blueprint agrupa rutas relacionadas. Esto evita tener todas las URLs en un solo archivo y facilita ubicar la logica de cada modulo.

## Separacion De Responsabilidades

La separacion general es:

- `routes/`: recibe requests, lee parametros, llama modelos y renderiza templates.
- `models/`: contiene acceso a base de datos, consultas y operaciones de persistencia.
- `templates/`: define HTML con Jinja2.
- `static/`: contiene CSS, JavaScript, Bootstrap local e imagenes.
- `compose.yaml`: define servicios, variables de entorno y red Docker.

Ejemplo de flujo normal:

1. El navegador pide `/`.
2. Flask dirige la request a `home_bp.py`.
3. La ruta consulta datos usando `queries_db.py`.
4. El modelo obtiene una conexion con `get_conn()`.
5. Se ejecuta SQL contra MariaDB.
6. La ruta renderiza `templates/index.html`.
7. `layout.html` carga CSS y JS desde `static/`.

## Base De Datos

La app usa MariaDB como fuente principal de datos. Las conexiones estan centralizadas en `src/app/models/db.py`.

Aunque el proyecto conserva archivos `.db` antiguos en la raiz y en `src/`, el codigo actual usa MariaDB mediante variables como:

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

El pooling se maneja con SQLAlchemy. Esto ayuda a evitar problemas de conexiones perdidas despues de mucho tiempo de inactividad.

## Templates Y Frontend

El frontend usa templates Jinja2. La plantilla principal es `src/app/templates/layout.html`.

Ese layout define:

- Estructura base HTML.
- Carga de Bootstrap local.
- Carga de `main.css` y `theme.css`.
- Navbar principal.
- Menu de apariencia.
- Links visibles segun sesion de usuario.
- Bloque `{% block content %}` para que cada vista inserte su contenido.

El comportamiento visual de temas se maneja con `static/js/themeAppearance.js` y atributos en el elemento HTML.

## Logging Tecnico De Requests

`src/app/routes/debug_bp.py` registra informacion tecnica de cada request y response.

El logging sigue saliendo por consola, lo que permite verlo con Docker Compose. Ademas, las requests no estaticas se guardan en la tabla `request_logs`.

Se capturan datos como:

- Metodo HTTP.
- Ruta.
- IP remota.
- Headers de proxy.
- User-Agent crudo.
- Navegador, plataforma y version cuando Flask puede inferirlo.
- Headers sanitizados.
- Body sanitizado u omitido si es grande.
- Status de response.
- Duracion en milisegundos.

Los headers y campos sensibles se redactan antes de loguear o guardar.

## Seguridad Basica

La app tiene varias medidas ya presentes:

- Login con Flask-Login.
- Proteccion CSRF global con Flask-WTF.
- Passwords almacenados con hash mediante Werkzeug.
- Blueprints administrativos protegidos por `current_user.is_authenticated`.
- Sanitizacion de datos sensibles en logs tecnicos.

Hay aspectos que podrian endurecerse mas adelante, como roles, permisos por accion y expiracion explicita de sesion.

## Puntos A Tener Presentes

- La app corre con el servidor de desarrollo de Flask en modo debug.
- Para un entorno productivo convendria usar Gunicorn, Waitress u otro servidor WSGI.
- Las tablas se crean desde codigo al arrancar o importar ciertos modulos.
- No hay sistema formal de migraciones de base de datos.
- El proyecto esta orientado a pruebas y aprendizaje, pero ya tiene una estructura razonable para crecer.
