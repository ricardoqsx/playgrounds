from models import *
from routes import *
from flask import Flask
from routes import *
from models import *

app = Flask(__name__)

app.register_blueprint(agenda)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9000', debug=True)