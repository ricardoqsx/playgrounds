from flask import render_template, request, redirect, url_for, Blueprint
from app.models.queries_db import *

home = Blueprint('home',__name__)

@home.route('/')
def index():
    cons = posts()
    return render_template('index.html',cons=cons)

# Ruta dinamica para visualizar articulos
@home.route('/<int:article_id>')
def read_story(article_id):
    # Obtenemos los datos del artículo
    article = read_article(article_id)
    if not article:
        return render_template('blog/404.html'), 404
    # Se pasa el artículo a la plantilla con el nombre 'article'
    return render_template('blog/article.html', article=article)