# playgrounds

- playground repo for test characteristics about flask

# Structure:

- this is a sample structure for every project we made

```
project/
├── app/
│   ├── __init__.py         # Configuración inicial de la app Flask
│   ├── models.py           # Definición de modelos (SQLAlchemy)
│   ├── routes/
│   │   ├── __init__.py     # Registro de blueprints
│   │   ├── auth.py         # Rutas relacionadas con autenticación
│   │   ├── admin.py        # Rutas para el dashboard y administración
│   │   ├── blog.py         # Rutas públicas para el blog
│   │   ├── reports.py      # Rutas para el reporteador
│   ├── templates/
│   │   ├── auth/           # Plantillas para login/registro
│   │   ├── admin/          # Plantillas para administración y dashboard
│   │   ├── blog/           # Plantillas públicas del blog
│   │   ├── reports/        # Plantillas del reporteador
│   │   ├── base.html       # Layout principal
│   │   ├── dashboard.html  # Layout para dashboard
│   ├── static/             # Archivos estáticos (CSS, JS, imágenes)
│   ├── forms.py            # Formularios WTForms
│   ├── utils.py            # Funciones auxiliares
│   ├── permissions.py      # Gestión de roles y permisos
│   ├── config.py           # Configuración del proyecto
├── migrations/             # Archivos de migraciones de base de datos
├── tests/                  # Pruebas unitarias
├── .env                    # Variables de entorno (credenciales, configs)
├── requirements.txt        # Dependencias del proyecto
├── run.py                  # Archivo principal para correr el servidor
└── README.md               # Documentación del proyecto
```

#### the thing about this repo is for make module standard code for work in other projects