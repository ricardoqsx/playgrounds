# Backend Y Rutas

El backend esta construido con Flask y organizado mediante blueprints. Cada blueprint agrupa rutas de una parte concreta de la aplicacion.

La idea principal es que las rutas no escriban SQL directamente. Las rutas leen datos de la request, aplican validaciones simples, llaman funciones de `models/` y luego devuelven HTML renderizado o una redireccion.

## Inicializacion De La App

Archivo principal: `src/app/__init__.py`.

La funcion `create_app()` construye la aplicacion Flask y registra los componentes principales:

- `LoginManager` para sesiones de usuario.
- `CSRFProtect` para proteger formularios.
- `secret_key` para sesiones y CSRF.
- `create_request_logs()` para asegurar la tabla de logs tecnicos.
- Blueprints de autenticacion, administracion, home, pruebas, debug y usuarios.
- Handlers para errores 401 y 404.

El loader de usuario se define con:

```python
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(id)
```

Esto permite que Flask-Login reconstruya el usuario actual a partir del ID guardado en la sesion.

## Registro Central De Blueprints

Los blueprints se exportan desde `src/app/routes/__init__.py`:

```python
from .auth_bp import *
from .admin_bp import *
from .home_bp import *
from .testing_bp import *
from .debug_bp import *
from .users_bp import *
```

Luego se registran dentro de `create_app()`:

```python
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(home)
app.register_blueprint(pruebas)
app.register_blueprint(debug_bp)
app.register_blueprint(users)
```

## Rutas Publicas Del Blog

Archivo: `src/app/routes/home_bp.py`.

Blueprint:

```python
home = Blueprint('home', __name__)
```

### `GET /`

Ruta: `index()`.

Responsabilidades:

- Leer el parametro de busqueda `q`.
- Leer el numero de pagina desde `page`.
- Consultar articulos normales o resultados de busqueda.
- Calcular total de paginas.
- Renderizar `templates/index.html`.

Funciones de modelo usadas:

- `total_articulos()`
- `posts()`
- `total_articulos_busqueda()`
- `buscar_posts()`

### `GET /<article_id>`

Ruta: `read_story(article_id)`.

Responsabilidades:

- Buscar un articulo por ID.
- Devolver 404 si no existe.
- Convertir el contenido Markdown a HTML.
- Renderizar `templates/blog/article.html`.

El contenido se convierte con:

```python
markdown.markdown(historia, extensions=['tables', 'fenced_code'])
```

## Rutas De Administracion De Articulos

Archivo: `src/app/routes/admin_bp.py`.

Blueprint:

```python
admin = Blueprint('admin', __name__, url_prefix='/admin')
```

Estas rutas estan protegidas por:

```python
@admin.before_request
def check_authenticated():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
```

Si el usuario no tiene sesion activa, se redirige al login.

### `GET /admin/`

Ruta: `home()`.

Responsabilidades:

- Mostrar listado administrativo de articulos.
- Permitir busqueda con `query`.
- Renderizar `templates/admin/home.html`.

### `GET /admin/<article_id>`

Ruta: `view_story(article_id)`.

Responsabilidades:

- Mostrar un articulo en vista administrativa.
- Devolver 404 si no existe.
- Renderizar `templates/admin/article.html`.

### `GET|POST /admin/insert`

Ruta: `insert()`.

Responsabilidades:

- En `GET`, mostrar el formulario de creacion.
- En `POST`, leer `titulo`, `categoria`, `autor` y `contenido`.
- Crear el articulo con `create_article()`.
- Redirigir a la misma vista.

### `GET /admin/edit`

Ruta: `edit()`.

Responsabilidades:

- Mostrar listado de articulos para editar.
- Permitir busqueda con `query`.
- Renderizar `templates/admin/edit.html`.

### `GET|POST /admin/edit/<article_id>`

Ruta: `edit_story(article_id)`.

Responsabilidades:

- En `GET`, cargar articulo y mostrar formulario completo.
- En `POST`, actualizar campos recibidos desde formulario.
- Redirigir a la vista de edicion del mismo articulo.

### `GET|POST /admin/delete`

Ruta: `delete()`.

Responsabilidades:

- En `GET`, listar articulos para borrar.
- En `POST`, leer la lista `ext` con IDs seleccionados.
- Llamar `delete_article()`.
- Redirigir a la vista de borrado.

## Rutas De Autenticacion

Archivo: `src/app/routes/auth_bp.py`.

Blueprint:

```python
auth = Blueprint('auth', __name__, url_prefix='/auth')
```

### `GET|POST /auth/`

Ruta: `login()`.

Responsabilidades:

- En `GET`, mostrar formulario de login.
- En `POST`, leer username y password.
- Validar campos vacios.
- Buscar usuario con `ModelUser.login()`.
- Crear sesion con `login_user()` si las credenciales son validas.
- Redirigir a `admin.home`.

### `GET|POST /auth/registro`

Ruta: `register()`.

Responsabilidades:

- Mostrar formulario de registro.
- Validar usuario/correo duplicado.
- Validar formato de correo.
- Validar fuerza de password.
- Crear usuario con password hasheado.
- Redirigir al login si el registro fue exitoso.

### `GET /auth/logout`

Ruta: `logout()`.

Responsabilidades:

- Cerrar sesion con `logout_user()`.
- Redirigir al login.

## Rutas De Usuarios

Archivo: `src/app/routes/users_bp.py`.

Blueprint:

```python
users = Blueprint('users', __name__, url_prefix='/users')
```

Este modulo tambien exige sesion activa con `current_user.is_authenticated`.

### `GET /users/`

Ruta: `inicio()`.

Responsabilidades:

- Consultar usuarios con `view_users()`.
- Renderizar `templates/users/index.html`.

### `GET /users/edit/<user_id>`

Ruta: `edit(user_id)`.

Responsabilidades:

- Buscar datos de un usuario.
- Devolver 404 si no existe.
- Renderizar `templates/users/edit.html`.

Actualmente esta ruta muestra informacion, pero no procesa actualizacion por `POST`.

### `GET|POST /users/delete`

Ruta: `delete()`.

Responsabilidades:

- En `GET`, listar usuarios.
- En `POST`, leer IDs seleccionados desde `ext`.
- Borrar usuarios con `delete_user()`.
- Redirigir a la misma vista.

## Ruta De Pruebas

Archivo: `src/app/routes/testing_bp.py`.

Blueprint:

```python
pruebas = Blueprint('pruebas', __name__, url_prefix='/pruebas')
```

### `GET /pruebas/test`

Renderiza `templates/blog/test.html`. Sirve como punto simple para pruebas visuales o funcionales.

## Debug Y Logging Tecnico

Archivo: `src/app/routes/debug_bp.py`.

Este blueprint no define una ruta visible. En su lugar, registra hooks globales:

```python
app.before_request(log_request_info)
app.after_request(log_response_info)
```

Eso significa que se ejecuta antes y despues de cada request.

### Antes De Cada Request

`log_request_info()`:

- Guarda el tiempo de inicio en `g.request_started_at`.
- Prepara el body para log.
- Loguea headers sanitizados.
- Loguea el body si es JSON pequeno.
- Omite bodies grandes o no relevantes.

### Despues De Cada Response

`log_response_info(response)`:

- Loguea headers de response.
- Omite HTML completo.
- Omite streams.
- Loguea cuerpos de response no HTML.
- Guarda la informacion en base de datos si la ruta no empieza por `/static/`.

### Sanitizacion

Los headers sensibles se reemplazan por `[redacted]`:

- `authorization`
- `cookie`
- `set-cookie`
- `x-csrftoken`
- `x-csrf-token`

Los campos sensibles del body tambien se redactan:

- `password`
- `passwd`
- `csrf_token`
- `token`
- `secret`

## Consideraciones De Seguridad

- Las rutas de admin y users requieren sesion activa.
- Los formularios estan protegidos por CSRF global.
- Las passwords no se guardan en texto plano.
- El debug evita guardar cookies y tokens reales.
- Todavia no hay roles o permisos granulares por tipo de usuario.
- El modo debug no deberia usarse como configuracion productiva.
