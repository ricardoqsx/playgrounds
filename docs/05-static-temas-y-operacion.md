# Static, Temas Y Operacion

Este documento cubre los archivos estaticos del proyecto y la forma en que se ejecuta con Docker Compose.

Los archivos estaticos viven en `src/app/static/`. Incluyen CSS, JavaScript, Bootstrap local e imagenes.

## Estructura De Static

```text
src/app/static/
├── css/
│   ├── bootstrap.min.css
│   ├── main.css
│   └── theme.css
├── js/
│   ├── bootstrap.bundle.min.js
│   └── themeAppearance.js
├── img/
│   ├── bg6.jpg
│   ├── pinwheel.png
│   └── star.png
└── utils/
    ├── bootstrap-grid.min.css
    ├── bootstrap-reboot.min.css
    └── bootstrap-utilities.min.css
```

Flask sirve estos archivos desde la ruta `/static/...`.

## Bootstrap Local

El proyecto no depende de CDN para Bootstrap. Los archivos se cargan localmente desde `static/`.

En `layout.html` se carga:

```jinja2
<link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
```

Y al final del body:

```jinja2
<script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
```

Esto hace que la interfaz funcione incluso sin depender de servicios externos para estilos base.

## `main.css`

Archivo: `src/app/static/css/main.css`.

Contiene ajustes generales y utilidades especificas del proyecto.

Responsabilidades principales:

- Altura y scroll de tablas.
- Ajustes para formularios de insercion.
- Altura maxima para listas de articulos.
- Estilo de bloque de requisitos de password.
- Personalizacion de scrollbars.
- Comportamiento visual del scroll en body.

Ejemplos de clases:

- `.scrollable-table`
- `.fit-insert`
- `.article-list`
- `.password-requirements`

Este archivo debe usarse para estilos puntuales de componentes o vistas.

## `theme.css`

Archivo: `src/app/static/css/theme.css`.

Define el sistema visual principal del sitio.

Usa variables CSS para controlar colores, fondos, bordes, sombras y textos:

```css
--cms-bg-main
--cms-bg-panel
--cms-line
--cms-text-main
--cms-accent
```

El tema se aplica a partir de atributos en el elemento `html`:

```html
<html data-theme="dark">
<html data-theme="light">
<html data-cms-bg-theme="teal">
```

## Tema Claro Y Oscuro

El archivo define dos grupos principales:

- `html[data-theme="dark"]`
- `html[data-theme="light"]`

Tambien hay un caso por defecto:

```css
html:not([data-theme]),
html[data-theme="dark"] {
    ...
}
```

Esto significa que si no hay tema guardado, la app cae al modo oscuro.

## Fondos Visuales

`theme.css` incluye varios fondos seleccionables:

- `base`
- `teal`
- `blue`
- `violet`
- `amber`
- `multi`
- `aqua`
- `spectrum`
- `slate`
- `copper`
- `sky`
- `purple`
- `rose`
- `lime`
- `indigo`
- `crimson`
- `ember`
- `sunset`
- `gold`
- `honey`
- `volcano`
- `coral`

Cada fondo se activa con `data-cms-bg-theme`.

Ejemplo:

```html
<html data-cms-bg-theme="violet">
```

El CSS tambien define variantes para tema claro cuando aplica.

## Selector De Apariencia

El selector esta en `layout.html`, dentro del menu `Apariencia`.

Tiene dos grupos:

- Tema: oscuro o claro.
- Fondos: lista de swatches visuales.

Cada boton usa atributos como:

```html
data-cms-theme="dark"
data-cms-bg-theme="teal"
```

Estos atributos son leidos por `themeAppearance.js`.

## `themeAppearance.js`

Archivo: `src/app/static/js/themeAppearance.js`.

Este script maneja el cambio de tema visual desde el navegador.

Responsabilidades:

- Leer tema guardado en `localStorage`.
- Validar que el tema exista en la lista permitida.
- Aplicar `data-theme` al `document.documentElement`.
- Aplicar `data-cms-bg-theme` para fondos.
- Guardar cambios del usuario en `localStorage`.
- Marcar botones activos con `.is-active`.
- Actualizar `aria-pressed` para accesibilidad.

Claves usadas en `localStorage`:

```text
playgrounds-theme
playgrounds-bg-theme
```

## Script Temprano En `layout.html`

Antes de cargar CSS, `layout.html` incluye un script pequeno que lee `localStorage` y coloca atributos en `html`.

Esto evita que la pagina pinte primero con un tema y luego cambie rapidamente a otro.

Es una tecnica simple para reducir parpadeos visuales.

## Imagenes

Carpeta: `src/app/static/img/`.

Archivos actuales:

- `star.png`: favicon usado por `layout.html`.
- `bg6.jpg`: imagen disponible para fondos o pruebas visuales.
- `pinwheel.png`: imagen disponible para vistas o pruebas.

Si se agregan mas imagenes, conviene mantener nombres claros y evitar archivos pesados innecesarios.

## Dockerfile

Archivo: `Dockerfile`.

Construye la imagen de la aplicacion:

```dockerfile
FROM python:alpine

WORKDIR /src

COPY ./src .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "run.py"]
```

Puntos importantes:

- El codigo corre desde `/src` dentro del contenedor.
- Las dependencias se instalan desde `src/requirements.txt`.
- Al cambiar requirements, hay que reconstruir la imagen.

## Docker Compose

Archivo: `compose.yaml`.

Define dos servicios principales:

- `mariadb`: base de datos.
- `playgrounds`: aplicacion Flask.

## Servicio MariaDB

Configuracion principal:

```yaml
mariadb:
  image: mariadb:11
  container_name: playgrounds-db
```

Variables:

```yaml
- MARIADB_DATABASE=playgrounds
- MARIADB_USER=playgrounds
- MARIADB_PASSWORD=playgrounds
- MARIADB_ROOT_PASSWORD=playgrounds-root
```

Usa volumen persistente:

```yaml
volumes:
  - mariadb-data:/var/lib/mysql
```

Esto permite conservar datos aunque el contenedor se recree.

## Healthcheck De MariaDB

MariaDB tiene healthcheck:

```yaml
healthcheck:
  test: ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"]
  interval: 10s
  timeout: 5s
  retries: 5
```

El servicio de Flask espera a que MariaDB este healthy antes de arrancar.

## Servicio Flask

Servicio:

```yaml
playgrounds:
  container_name: playgrounds
  build: .
  image: playgrounds:latest
```

Expone:

```yaml
ports:
  - 8050:8050
```

Monta el codigo local:

```yaml
volumes:
  - ./src:/src
```

Esto permite modificar codigo local y reflejarlo dentro del contenedor durante desarrollo.

## Variables De Base De Datos En La App

El servicio `playgrounds` define:

```yaml
- DB_HOST=mariadb
- DB_PORT=3306
- DB_NAME=playgrounds
- DB_USER=playgrounds
- DB_PASSWORD=playgrounds
```

Estas variables son leidas desde `models/db.py`.

## Variables Del Pool

Tambien estan visibles en `compose.yaml`:

```yaml
- DB_POOL_SIZE=5
- DB_MAX_OVERFLOW=10
- DB_POOL_TIMEOUT=30
- DB_POOL_RECYCLE=1800
- DB_CONNECT_TIMEOUT=10
- DB_READ_TIMEOUT=30
- DB_WRITE_TIMEOUT=30
```

Estas variables controlan como se reutilizan conexiones a MariaDB.

Cuando se muevan a `.env`, la idea sera mantener los mismos nombres y referenciarlos desde Compose.

## Reinicio De Contenedores

Ambos servicios usan:

```yaml
restart: unless-stopped
```

Esto indica que Docker debe reiniciar los contenedores si caen, salvo que hayan sido detenidos manualmente.

## Traefik

El servicio `playgrounds` incluye labels para Traefik:

```yaml
- "traefik.enable=true"
- "traefik.http.routers.playgrounds.rule=Host(`playgrounds.mirai.local`)"
- "traefik.http.routers.playgrounds.entrypoints=web"
- "traefik.http.services.playgrounds.loadbalancer.server.port=8050"
```

Esto permite enrutar trafico hacia el contenedor desde Traefik usando el host configurado.

La red usada es externa:

```yaml
networks:
  traefik-net:
    external: true
```

## Comandos De Operacion

Levantar y reconstruir:

```bash
docker compose up --build
```

Levantar en segundo plano:

```bash
docker compose up -d --build
```

Ver logs:

```bash
docker compose logs -f playgrounds
```

Ver logs de MariaDB:

```bash
docker compose logs -f mariadb
```

Bajar servicios:

```bash
docker compose down
```

## Notas De Mantenimiento

- Si cambia `requirements.txt`, reconstruir imagen.
- Si cambia solo codigo Python y el volumen esta montado, normalmente basta con reiniciar la app.
- Si se cambia el schema de una tabla existente, `CREATE TABLE IF NOT EXISTS` no aplicara cambios de columnas.
- Si se cambian variables de entorno, hay que recrear el contenedor.
- Los requests a `/static/...` no se guardan en `request_logs` para evitar ruido.

## Consideracion Sobre Produccion

La app actualmente corre con Flask debug server:

```python
app.run(host='0.0.0.0', port='8050', debug=True)
```

Esto esta bien para desarrollo y pruebas. Para produccion convendria usar un servidor WSGI como Gunicorn o Waitress y desactivar debug.
