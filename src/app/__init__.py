from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configuraciones (BD, blueprints, etc.)
    from app.routes.agenda import agenda  # Importar blueprint
    app.register_blueprint(agenda)
    return app