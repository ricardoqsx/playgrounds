from flask import render_template, request, Blueprint
from math import ceil
import markdown
from app.models.queries_db import *

home = Blueprint('home',__name__)

@home.route('/')
def index():
    # Capturamos el término de búsqueda si existe
    search_term = request.args.get('q', None)
    # Obtenemos la página actual desde la URL (ej: ?page=2)
    pagina = request.args.get('page', 1, type=int)
    # Cantidad de artículos por página, tambien se debe modificar en queries_db
    por_pagina = 8

    # Lógica diferenciada para búsqueda/normal
    if search_term:
        # Función nueva para contar resultados de búsqueda
        total = total_articulos_busqueda(search_term)
        # Función nueva para buscar con paginación
        articulos = buscar_posts(search_term, pagina, por_pagina)
    else:
        # Funciones existentes
        total = total_articulos()
        articulos = posts(pagina, por_pagina)

    # Cálculo de páginas (igual que antes pero con el total correspondiente)
    total_paginas = ceil(total / por_pagina)
    pagina = max(1, min(pagina, total_paginas))

    return render_template(
        'index.html',
        cons=articulos,
        pagina_actual=pagina,
        total_paginas=total_paginas,
        search_term=search_term)  # Pasamos el término al template

# Ruta dinamica para visualizar articulos
@home.route('/<int:article_id>')
def read_story(article_id):
    # Obtenemos los datos del artículo
    article = read_article(article_id)
    md = markdown.markdown(article[4], extensions=['tables', 'fenced_code'])
    if not article:
        return render_template('utils/404.html'), 404
    # Se pasa el artículo a la plantilla con el nombre 'article'
    return render_template('blog/article.html', article=article, md=md)