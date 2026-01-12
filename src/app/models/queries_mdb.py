from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://pyuser:pypass@playdb:3306/playdb?charset=utf8mb4"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    db.init_app(app)