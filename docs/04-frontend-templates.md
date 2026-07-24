# Frontend Y Templates

El frontend del proyecto esta construido con templates Jinja2 renderizados desde Flask. No hay framework frontend separado. La navegacion, formularios y vistas se generan desde archivos HTML ubicados en `src/app/templates/`.

La parte visual se apoya en Bootstrap local y CSS propio.

## Layout Base

Archivo: `src/app/templates/layout.html`.

Este archivo define la estructura comun de todas las paginas.

Responsabilidades principales:

- Definir `DOCTYPE`, idioma, charset y viewport.
- Cargar favicon desde `static/img/star.png`.
- Inicializar tema oscuro/claro antes de pintar la pagina.
- Cargar Bootstrap local.
- Cargar `main.css` y `theme.css`.
- Renderizar la navbar principal.
- Mostrar links segun el estado de autenticacion.
- Exponer el bloque `{% block content %}`.
- Cargar JavaScript de Bootstrap y `themeAppearance.js`.

## Herencia Con Jinja2

Las vistas usan herencia de templates. El patron esperado es:

```jinja2
{% extends 'layout.html' %}

{% block content %}
  contenido de la vista
{% endblock %}
```

Esto permite que todas las paginas compartan navbar, estilos, scripts y estructura general.

## Navbar Principal

La navbar vive en `layout.html`.

Incluye:

- Link principal a `/`.
- Menu de apariencia.
- Link a login.
- Link a pruebas.
- Menu de operaciones si el usuario esta autenticado.
- Buscador visible solo en la vista publica del home.

La condicion para mostrar operaciones es:

```jinja2
{% if current_user.is_authenticated %}
```

Esto conecta directamente con Flask-Login.

## Buscador Publico

El buscador aparece solo cuando la ruta actual es `home.index`:

```jinja2
{% if request.endpoint == 'home.index' %}
```

Envia datos por `GET` hacia `home.index` usando el parametro `q`.

Ese valor se lee en `home_bp.py` como:

```python
search_term = request.args.get('q', None)
```

## Templates Publicos

### `templates/index.html`

Vista principal del blog.

Recibe desde `home_bp.py`:

- `cons`: articulos a mostrar.
- `pagina_actual`: pagina activa.
- `total_paginas`: total de paginas disponibles.
- `search_term`: termino buscado.

Su objetivo es listar articulos y permitir navegacion paginada.

### `templates/blog/article.html`

Vista publica de articulo individual.

Recibe:

- `article`: tupla con datos del articulo.
- `md`: contenido convertido desde Markdown a HTML.

Se usa para mostrar el contenido completo de una historia.

### `templates/blog/test.html`

Vista usada por `/pruebas/test`. Sirve como espacio de pruebas.

### `templates/blog/comment.html`

Archivo reservado para comentarios o pruebas relacionadas. Actualmente no aparece conectado a una ruta principal en el flujo revisado.

## Templates De Utilidad

Carpeta: `templates/utils/`.

Archivos principales:

- `401.html`: vista para errores de autorizacion.
- `404.html`: vista para recurso no encontrado.
- `categories.html`: utilidad visual o parcial relacionado con categorias.
- `search_panel.html`: panel reutilizable de busqueda.
- `pawg.html`: archivo utilitario o experimental.

Los errores se conectan desde `auth_bp.py`:

```python
def status_404(error):
    return render_template('utils/404.html'), 404

def status_401(error):
    return render_template('utils/401.html'), 401
```

Luego se registran en `create_app()`.

## Templates De Autenticacion

Carpeta: `templates/auth/`.

### `auth/login.html`

Vista de login.

Recibe mensajes `flash()` desde `auth_bp.py` cuando:

- faltan campos;
- usuario o password son incorrectos.

El formulario envia `POST` a `/auth/`.

## Templates De Registro Y Usuarios

Carpeta: `templates/users/`.

### `users/register.html`

Vista de registro de usuario.

Se usa desde `auth.register()`.

Puede recibir:

- `form_data`: datos del formulario cuando ocurre una validacion fallida.
- mensajes flash de error o exito.

Validaciones relacionadas:

- usuario/correo duplicado;
- formato de email;
- fuerza de password.

### `users/index.html`

Lista usuarios registrados.

Recibe:

- `users`: resultado de `view_users()`.

### `users/edit.html`

Muestra informacion de un usuario especifico.

Recibe:

- `users`: resultado de `edit_users(user_id)`.

### `users/delete.html`

Permite seleccionar usuarios para borrar.

Recibe:

- `frontquery`: listado de usuarios.

El formulario envia una lista de IDs bajo el nombre `ext`.

## Templates Administrativos

Carpeta: `templates/admin/`.

Estas vistas estan protegidas por el blueprint `admin`, que exige sesion activa.

### `admin/home.html`

Vista principal de articulos en administracion.

Recibe:

- `frontblog`: listado de articulos.

### `admin/article.html`

Vista administrativa de articulo individual.

Recibe:

- `article`: datos del articulo.

### `admin/insert.html`

Formulario de creacion de articulos.

Campos esperados por backend:

- `titulo`
- `categoria`
- `autor`
- `contenido`

### `admin/edit.html`

Listado de articulos para seleccionar cual editar.

Recibe:

- `frontblog`: listado de articulos.

### `admin/edit_full.html`

Formulario completo para editar un articulo.

Campos esperados por backend:

- `ids`
- `titulo`
- `categoria`
- `autor`
- `contenido`

### `admin/delete.html`

Vista para seleccionar articulos a eliminar.

Recibe:

- `frontquery`: listado de articulos.

El formulario envia IDs seleccionados bajo el nombre `ext`.

### `admin/404.html`

Vista de error usada por algunas rutas administrativas cuando un articulo no existe.

## Contrato Entre Rutas Y Templates

Cada ruta debe pasar al template las variables que este espera. Si se cambia un nombre en backend, tambien debe cambiarse en el template.

Ejemplos actuales:

- `home.index` pasa `cons`, `pagina_actual`, `total_paginas`, `search_term`.
- `admin.home` pasa `frontblog`.
- `admin.delete` pasa `frontquery`.
- `users.inicio` pasa `users`.
- `users.delete` pasa `frontquery`.

Mantener estos nombres consistentes evita errores de renderizado y vistas vacias.

## Consideraciones De Accesibilidad Y Uso

- El layout define `lang="es"`.
- La navbar usa elementos Bootstrap responsivos.
- El selector de apariencia usa botones y atributos `aria-label` en fondos.
- El buscador usa `role="search"` y `aria-label`.

Para futuras vistas conviene mantener:

- labels claros en formularios;
- mensajes visibles de error;
- botones con texto comprensible;
- navegacion usable en mobile.

## Mantenimiento Recomendado

- Evitar duplicar navbar o imports de CSS en templates hijos.
- Mantener formularios alineados con nombres esperados por rutas.
- Si una vista crece demasiado, extraer parciales a `templates/utils/`.
- Evitar incluir logica de negocio compleja dentro de Jinja.
- Las validaciones importantes deben seguir en backend, no solo en HTML.
