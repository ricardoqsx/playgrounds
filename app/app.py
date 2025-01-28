from flask import Flask
from routes.agenda import agenda_bp

app=Flask(__name__)

app.register_blueprint(agenda_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6000', debug=True)