from flask import Flask
import os
from app.routes import *  # Importar blueprint

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
    # Configuraciones (BD, blueprints, etc.)
    app.register_blueprint(admin)
    app.register_blueprint(home)
    return app