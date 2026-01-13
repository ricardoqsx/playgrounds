import os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://pyuser:pypass@playdb:3306/playdb?charset=utf8mb4"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    db.init_app(app)

class Blog(db.Model):
    __tablename__ = "blog"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(255), nullable=False)
    historia = db.Column(db.Text, nullable=False)

def create_blog():
    db.create_all()
    if db.session.query(Blog).count() == 0:
        current_dir = os.path.dirname(__file__)
        csv_path = os.path.join(current_dir, "blog.csv")
        df = pd.read_csv(csv_path)
        columns_to_insert = ['id','titulo','categoria','autor','historia']
        records = [
            Blog(**row)
            for row in df[columns_to_insert].to_dict(orient="records")
        ]
        db.session.add_all(records)
        db.session.commit()
