from routes.agenda import *

def register_blueprints(app):
    # Registrar blueprints aquí
    app.register_blueprint(agenda_bp)