from .agenda import agenda_bp

def register_blueprints(app):
    # Registrar blueprints aquí
    app.register_blueprint(agenda_bp)