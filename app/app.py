from flask import Flask
from routes import register_blueprints
from models.contacts_db import contacts_db

contacts_db.create_db()

def create_app():
    app=Flask(__name__)

    # Registro de blueprints
    register_blueprints(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6000', debug=True)