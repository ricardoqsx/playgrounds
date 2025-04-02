# Playgrounds

- playgrounds repo para pruebas de caracteristicas de flask

## _*Estructura del proyecto*_

```
playgrounds/                                       # Proyecto Playgrounds, raiz
├── compose.yaml                                   # Archivo estructural que contiene las instrucciones para deploy
├── Dockerfile                                     # Archivo de construccion de la imagen
├── LICENSE                                        # Licencias usadas (GPL en este caso)
├── README.md                                      # Explicacion del proyecto
├── restart.sh                                     # script para automatizar deploy
└── src                                            # Toda la app esta aqui
    ├── app                                        # Carpeta App
    │   ├── __init__.py                            # Archivo init que modulariza app
    │   ├── models                                 # Carpeta models
    │   │   ├── blog.csv                           # Datos de prueba
    │   │   ├── blog_db.py                         # Consultas a utilizar para trabajar con la BD
    │   │   └── __init__.py                        # Archivo init que modulariza models
    │   ├── routes                                 # Carpeta/Modulo routes
    │   │   ├── admin_bluep.py                     # Ruta Administrativa
    │   │   ├── home_bluep.py                      # Ruta home
    │   │   └── __init__.py                        # Archivo init que modulariza routes
    │   ├── static                                 # Archivos estaticos
    │   │   ├── css                                # Utilidades de css para estilos
    │   │   │   ├── bootstrap-grid.min.css         
    │   │   │   ├── bootstrap.min.css              
    │   │   │   ├── bootstrap-reboot.min.css       
    │   │   │   ├── bootstrap-utilities.min.css    
    │   │   │   └── main.css                       # Codigo css personalizado
    │   │   └── img                                # Imagenes varias
    │   │       ├── bg6.jpg
    │   │       └── star.png
    │   └── templates                              # Plantillas html para servir al cliente
    │       ├── admin                              # Ruta de consultas administrativas
    │       │   ├── 404.html                       # Vista 404 para cuando no existe un articulo, sirve esto
    │       │   ├── article.html                   # Plantilla para articulos
    │       │   ├── delete.html                    # Vista para el Borrado de articulos
    │       │   ├── edit_full.html                 # Vista individual para edicion de articulos
    │       │   ├── edit.html                      # Vista general para seleccionar cual articulo editar
    │       │   ├── home.html                      # Vista general de articulos
    │       │   └── insert.html                    # Vista para agregar un nuevo articulo
    │       ├── index.html                         # Vista de inicio
    │       ├── layout.html                        # Plantilla estructural
    │       └── search_panel.html                  # Panel modularizado
    ├── blog.db                                    # Base de datos del blog
    ├── requirements.txt                           # Requerimientos python necesarios para el proyecto
    └── run.py                                     # Archivo que inicia la aplicacion

9 directories, 32 files
```
---

## Explicacion Step by Step

El deploy inicia con el archivo compose, el cual al ejecutarse, inicia la construccion de la imagen mediante el Dockerfile y designa los parametros de como se ejecutara ese contenedor, en el dockerfile instala todas las dependencias en el servidor para que el app pueda correr sin inconvenientes. a partir de que el app esta funcionando, hay un volumen creado el cual actua como enlace entre los archivos fuente, y el contenedor.

A partir de aqui actuan los archivos .py que son la escencia de la aplicacion. la estructura basica seria asi:

- run.py crea la aplicacion y la despliega
- /app/__init__.py convierte en modulo todo lo que existe dentro de app (models, routes)
- /app/models/__init__.py convierte en modulo esta carpeta para disponer de las funciones de blog_db.py
- /app/models/blog_db.py contiene las operaciones a realizar en la base de datos
- /app/routes/__init__.py convierte en modulo esta carpeta para administrar las rutas con blueprints
- /app/routes/admin_bluep.py contiene las rutas que se usaran en el modulo de administracion
- /app/routes/home_bluep.py aqui estan las rutas de index y en general la vista de los usuarios

Adicional, tenemos distintas carpetas que sirven archivos estaticos para que al recibir peticiones, el servidor sirva

- /app/static contiene archivos css e imagenes para el estilizado
- /app/templates contiene los distintos archivos html, tanto plantillas como vistas

#### the thing about this repo is for make module standard code for work in other projects

## _*Razones para Usar Python, MySQL y Docker en la Creación de Aplicaciones*_

Al momento de desarrollar aplicaciones como una agenda o un CMS basado en Flask, es crucial elegir las tecnologías que mejor se adapten a las necesidades del proyecto. A continuación, se detallan los beneficios de usar Python, MySQL y Docker en este contexto:

---

### _*Python: La Base del Desarrollo*_
1. *Simplicidad y legibilidad*:
   Python es conocido por su sintaxis clara y fácil de entender. Esto facilita la colaboración entre desarrolladores y reduce el tiempo necesario para escribir y mantener el código.

2. *Frameworks robustos*:
   Herramientas como Flask y Django permiten crear aplicaciones web de forma eficiente y escalable. Flask, en particular, es ideal para proyectos pequeños y medianos debido a su flexibilidad y simplicidad.

3. *Amplia comunidad y recursos*:
   Python cuenta con una comunidad activa que ofrece bibliotecas, documentación y soporte técnico para casi cualquier necesidad, desde gestión de datos hasta aprendizaje automático.

4. *Interoperabilidad*:
   Python se integra fácilmente con otros lenguajes y tecnologías, lo que lo convierte en una opción versátil para proyectos que requieren múltiples herramientas.

---

### _*MySQL: Gestión de Datos Confiable*_
1. **Estabilidad y rendimiento**:
   MySQL es una de las bases de datos relacionales más utilizadas, reconocida por su capacidad de manejar grandes volúmenes de datos con rapidez y confiabilidad.

2. *Compatibilidad con Python*:
   Existen múltiples bibliotecas, como `mysql-connector` y `SQLAlchemy`, que permiten la integración sencilla de MySQL con aplicaciones Python.

3. *Flexibilidad en el diseño*:
   MySQL admite estructuras de datos complejas y permite realizar consultas avanzadas, lo que es esencial para aplicaciones como agendas o CMS que requieren operaciones sofisticadas con los datos.

4. *Soporte y comunidad*:
   Al ser una tecnología ampliamente adoptada, MySQL tiene una comunidad extensa que ofrece soluciones y soporte constante.

---

### _*Docker: Estandarización y Escalabilidad*_
1. *Entornos consistentes*:
   Docker permite crear contenedores que aseguran que la aplicación funcione de manera idéntica en cualquier entorno, ya sea desarrollo, pruebas o producción.

2. *Portabilidad*:
   Los contenedores Docker pueden ejecutarse en cualquier sistema operativo que soporte Docker, lo que elimina problemas de compatibilidad.

3. *Fácil integración y despliegue*:
   Con Docker, puedes empaquetar tu aplicación y sus dependencias en una imagen que se despliega de forma rápida y confiable, lo que reduce errores y tiempo de implementación.

4. *Escalabilidad*:
   Docker facilita la creación de aplicaciones escalables mediante la implementación de múltiples contenedores para manejar aumentos en la carga de trabajo.

5. *Ahorro de recursos*:
   A diferencia de las máquinas virtuales tradicionales, los contenedores son ligeros y consumen menos recursos, lo que es ideal para proyectos que requieren optimización.

---

## _*Objetivos del proyecto*_

## _*Alcance y descripcion de funcionalidades*_

- tendra 2 CRUD's, uno para usuarios, uno para los articulos
- los usuarios tendran diferente nivel de permisos (super usuario, admin, normal user)
- se debe trabajar en 2 modelos, uno para administradores y uno para el usuario comun
- se deben crear pantallas para crear articulos, e incluir imagenes y videos (delimitando el ancho)

---

### _*Conclusión*_
Al combinar Python, MySQL y Docker, obtienes un ecosistema potente y eficiente para desarrollar aplicaciones modernas. Python proporciona una base sólida y flexible, MySQL asegura la gestión confiable de datos, y Docker simplifica la implementación y escalabilidad. Esta combinación no solo optimiza el proceso de desarrollo, sino que también asegura que las aplicaciones sean portables, escalables y fáciles de mantener.