# Plan de trabajo (borrador vivo)

## Contexto rápido del repo
- Flask con blueprints (`home`, `admin`, `auth`, `users`, `pruebas`, `debug`), sin ORM; acceso directo a SQLite (`blog.db`, `user.db`) vía `sqlite3`.
- Modelos/consultas en `src/app/models/*`, templates en `src/app/templates/*`, assets en `src/app/static/*`.
- Autenticación con `flask-login` y creación inicial de datos en `create_blog()` y `create_users()` (se ejecutan al importar).
- Dockerfile ligero basado en `python:alpine`; `compose.yaml` solo levanta la app y monta `./src`.

## Suposiciones y preguntas abiertas (aclaradas)
- Roles definidos: `administrador` (todo), `profesor` (CRUD artículos), `editor` (crear/actualizar solo sus artículos), `lector` (solo comentarios). Todos pueden crear comentarios, solo admin aprueba/visibiliza.
- SMTP: se debe permitir configurar cuentas Gmail u Outlook/Office365 (SMTP autenticado). No se requiere verificación de remitente adicional; el remitente será tipo `noreply`. Si el servidor responde que el usuario no existe, no se registra la configuración.
- Dashboard: métricas de artículos (por categoría/autor), usuarios y sesiones, y eventos básicos; aceptado como base.
- Markdown: hay que sanitizar tanto el detalle como los previews (hoy se renderiza Markdown sin sanitizar para detalle y el preview es texto truncado sin parseo).

## Pila de trabajo (mini tareas incrementales)

1) **Base y configuración**
- Centralizar configuración vía `.env`/`config.py` (SECRET_KEY, DB_URI, SMTP) y quitar lógica de creación de datos en tiempo de import.
- Añadir `pip-tools`/`requirements-dev.txt` y scripts básicos (`makefile` o `scripts/*.sh`) para dev.
- Documentar arranque local (Flask) y en contenedor.

2) **Migración de SQLite a MariaDB + soporte multi motor**
- Elegir capa de acceso (recomendado: SQLAlchemy + Alembic); mapear `User`, `Blog` y futuras `Comments` (consultas actuales son CRUD simples, mapeables sin problemas).
- Crear `config.py` con `SQLALCHEMY_DATABASE_URI` y permitir seleccionar motor por env (`sqlite:///...`, `mysql+pymysql://...`, `mariadb+pymysql://...`).
- Actualizar `Dockerfile`/`compose.yaml` para agregar servicio MariaDB, variables de entorno, volúmenes y healthchecks; mantener SQLite usable en modo dev.
- Crear migraciones iniciales (schema en MariaDB) y script de migración de datos desde SQLite -> MariaDB.
- Refactorizar consultas crudas a ORM/engine único; eliminar dependencias directas a `sqlite3`.
- Pruebas de humo: login, CRUD de artículos, listado de usuarios.

3) **Roles y autorizaciones**
- Extender esquema `user` con tabla `roles` y tabla puente (soportar `administrador`, `profesor`, `editor`, `lector`).
- Semillas: crear roles y asignar admin al usuario inicial; `profesor` puede CRUD artículos; `editor` solo crea/edita propios; `lector` solo comenta; solo admin aprueba comentarios.
- Middleware/decoradores para proteger rutas por rol y ownership (autor del artículo) y actualizar blueprints (`admin`, `users`, futuros `comments`).
- Ajustar UI (navbar y vistas) para ocultar/mostrar acciones según rol y mostrar estado de aprobación de comentarios.
- Tests mínimos de autorización (por rol y por ownership).

4) **Recuperación de contraseña y correo remitente configurable**
- Definir tabla `email_settings` (o campos en `user`) para guardar remitente SMTP proporcionado por el usuario + estado de verificación (compatible con Gmail/Outlook/Office365).
- Implementar formulario para cargar credenciales SMTP (host/puerto/usuario/app password), envío de correo de prueba y persistir estado.
- Flujo de reset: formulario de solicitud, generación de token firmado, envío de correo, pantalla de nueva contraseña.
- Manejo seguro de credenciales (no guardarlas en claro; enmascarar en UI), rate limiting básico y logging de fallos de envío.

5) **Dashboard de estadísticas**
- Definir métricas iniciales: total de artículos, artículos por categoría/autor, usuarios por rol, últimos logins, comentarios pendientes/aprobados.
- Crear endpoints/consultas (ORM) y vista protegida para el dashboard.
- Elegir librería ligera (p.ej. Chart.js) e integrar con plantilla.
- Añadir pruebas de consultas y validaciones de permisos.

6) **Inicio con resúmenes en Markdown**
- Almacenar contenido en Markdown (ya se usa para detalle); para el listado, generar resumen seguro: parsear Markdown -> HTML y truncar con sanitización.
- Ajustar consulta de `posts()` para devolver preview seguro y templates para renderizarlo.
- Añadir sanitización explícita en detalle y preview; tests de renderizado para prevenir XSS/breaking layout.

7) **Calidad y operaciones**
- Añadir lint/format (ruff/black) y tests básicos (pytest) para auth, roles y posts.
- Configurar logging estructurado (ya hay `debug_bp`) y rutas de salud para contenedores.
- Opcional: pipeline de CI simple (lint + tests).

8) **Backups de base de datos**
- Implementar comando/endpoint protegido para backup completo del motor activo (MariaDB o SQLite) y ofrecer descarga del archivo.
- En MariaDB: usar `mysqldump` dentro del contenedor o `mariadb-dump` según imagen; en SQLite: copia del `.db`.
- Controlar permisos (solo admin), registrar auditoría de descargas y sanitizar nombres/paths de archivos.

## Backlog abierto (para agregar/quitar luego)
- Comentarios con moderación y paginación.
- Carga de imágenes/archivos para artículos (con límites de tamaño).
- Internacionalización de mensajes y plantillas.
- Métricas de correo (entregas/errores) y almacenamiento seguro de credenciales.

## Tareas técnicas siguientes (granulares)
- Configuración central: crear `config.py` y `.env.example`; mover `SECRET_KEY`, `DB_URI`, SMTP y flags. Actualizar `src/run.py` y `app/__init__.py` para leer config en vez de `os.environ` directo.
- Capa de datos: introducir SQLAlchemy en `app/models/` con modelos `User`, `Role`, `UserRole`, `Blog`, `Comment`, `EmailSettings`; mantener compatibilidad SQLite/MariaDB vía URIs.
- Migraciones: añadir Alembic, generar migración inicial (usuarios, roles, artículos, comentarios, email_settings). Crear script de migración de datos leyendo `user.db` y `blog.db` actuales.
- Blueprints/rutas: agregar blueprint `comments` y rutas REST básicas (crear, listar por artículo, aprobar). Ajustar `admin_bp.py`/`home_bp.py` para mostrar estado de aprobación y filtrar por rol/autor.
- Autorización: añadir decoradores (p.ej. `@require_role` y `@require_owner_or_role`) y usarlos en rutas `admin`, `users`, `comments`.
- Markdown y sanitización: incorporar librería de sanitizado (p.ej. `bleach`) en el render de detalle (`home_bp.read_story`) y en generación de previews en consultas `posts()` (pasar por markdown + bleach antes de truncar).
- SMTP y reset: crear rutas/forms para configurar SMTP (`/email/settings`), enviar prueba, y flujo de reset (`/auth/reset/request`, `/auth/reset/<token>`); usar `itsdangerous` para token firmado.
- Dashboard: nueva ruta en `admin` (p.ej. `/admin/dashboard`) con queries ORM para métricas (artículos por categoría/autor, usuarios por rol, comentarios pendientes/aprobados, últimos logins).
- Backups: ruta/endpoint protegido (`/admin/backups/db`) que ejecuta `sqlite` copy o `mysqldump` dentro del contenedor, entrega archivo descargable y registra auditoría.
