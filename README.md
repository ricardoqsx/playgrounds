# playgrounds

- playground repo for test characteristics about flask
- this is a sample structure for every project we made


```
playgrounds/                                     # root of the project
├── compose.yaml                                 # compose file to deploy the project
├── Dockerfile                                   # docker file to create the image
├── LICENSE
├── README.md
├── restart.sh                                   # tiny script for restart services
└── src/                                         # all the app is here
    ├── app/                                     # all the modules is inside
    │   ├── __init__.py
    │   ├── models/                              # database operations for call from routes
    │   │   ├── agenda.csv
    │   │   ├── contacts_db.py
    │   │   └── __init__.py
    │   ├── routes/                              # blueprints
    │   │   ├── agenda.py
    │   │   └── __init__.py
    │   ├── static/                              # css and img files
    │   │   ├── css/                             # css files
    │   │   │   ├── bootstrap-grid.min.css
    │   │   │   ├── bootstrap.min.css
    │   │   │   ├── bootstrap-reboot.min.css
    │   │   │   ├── bootstrap-utilities.min.css
    │   │   │   └── main.css
    │   │   └── img/                             # image files
    │   │       └── bg6.jpg
    │   └── templates/                           # routes where html are in
    │       ├── admin/                           # admin files that require elevation
    │       │   ├── delete.html
    │       │   ├── insert.html
    │       │   └── update.html
    │       ├── auth/                            # login and other stuff
    │       ├── blog/                            # templates for blog articles
    │       ├── index.html
    │       ├── layout.html
    │       └── reports/                         # reports and dashboard
    ├── requirements.txt
    └── run.py                                   # main app

16 directories, 29 files
```

#### the thing about this repo is for make module standard code for work in other projects