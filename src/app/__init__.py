from flask import Flask
from app.routes import *  # Importar blueprint

def create_app():
    app = Flask(__name__)
    # Configuraciones (BD, blueprints, etc.)
    app.register_blueprint(admin)
    app.register_blueprint(root)
    return app