# Playgrounds

- playgrounds repo para pruebas de caracteristicas de flask

## _*Estructura del proyecto*_

```
playgrounds/                                     # raiz del proyecto
├── compose.yaml                                 # compose para hacer el deploy
├── Dockerfile                                   # Dockerfile para crear contenedor
├── LICENSE
├── README.md
├── restart.sh                                   # script para pruebas
└── src/                                         # todo esto es el app
    ├── app/                                     # todos los modulos estan aqui
    │   ├── __init__.py
    │   ├── models/                              # operaciones de la DB para llamar desde rutas
    │   │   ├── agenda.csv
    │   │   ├── contacts_db.py
    │   │   └── __init__.py
    │   ├── routes/                              # blueprints
    │   │   ├── admin_bp.py
    │   │   └── __init__.py
    │   ├── static/                              # css e imagenes
    │   │   ├── css/                             # archivos css
    │   │   │   ├── bootstrap-grid.min.css
    │   │   │   ├── bootstrap.min.css
    │   │   │   ├── bootstrap-reboot.min.css
    │   │   │   ├── bootstrap-utilities.min.css
    │   │   │   └── main.css
    │   │   └── img/                             # imagenes
    │   │       └── bg6.jpg
    │   └── templates/                           # rutas donde estan los html
    │       ├── admin/                           # archivos admin que requieren permisos
    │       │   ├── delete.html
    │       │   ├── insert.html
    │       │   └── update.html
    │       ├── auth/                            # login y asi
    │       ├── blog/                            # plantillas para el blog
    │       ├── index.html
    │       ├── layout.html
    │       └── reports/                         # reportes y dashboard
    ├── requirements.txt
    └── run.py                                   # app principal

16 directorios, 29 archivos
```
---

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