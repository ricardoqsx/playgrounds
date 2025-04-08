from flask import render_template, request, redirect, url_for, Blueprint
from math import ceil
from app.models.queries_db import *

home = Blueprint('home',__name__)

@home.route('/')
def index():
    # Obtenemos la página actual desde la URL (ej: ?page=2)
    pagina = request.args.get('page', 1, type=int)
    por_pagina = 8  # Cantidad de artículos por página, tambien se debe modificar en queries_db
    
    total = total_articulos()
    total_paginas = ceil(total / por_pagina)
    
    # Aseguramos que la página esté dentro del rango válido
    pagina = max(1, min(pagina, total_paginas))
    
    # Obtenemos los posts de la página actual
    articulos = posts(pagina, por_pagina)
    
    return render_template(
        'index.html',
        cons=articulos,
        pagina_actual=pagina,
        total_paginas=total_paginas)

# Ruta dinamica para visualizar articulos
@home.route('/<int:article_id>')
def read_story(article_id):
    # Obtenemos los datos del artículo
    article = read_article(article_id)
    if not article:
        return render_template('blog/404.html'), 404
    # Se pasa el artículo a la plantilla con el nombre 'article'
    return render_template('blog/article.html', article=article)