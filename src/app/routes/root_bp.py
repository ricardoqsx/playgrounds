from flask import render_template, request, redirect, url_for, Blueprint
from app.models.agenda_db import *
from app.models.blog_db import *

create_blog()

root = Blueprint('root',__name__)

#Inicio
@root.route('/')
def home():
    search_query = request.args.get('query', '') 
    if search_query:
        frontblog = search_blog(search_query)
    else:
        frontblog = blogquery()
    return render_template('blog/home.html', frontblog=frontblog)

# Ruta dinamica para visualizar articulos
@root.route('/<int:article_id>')
def view_story(article_id):
    # Obtenemos los datos del artículo
    article = get_article(article_id)
    if not article:
        return render_template('blog/404.html'), 404
    # Se pasa el artículo a la plantilla con el nombre 'article'
    return render_template('blog/article.html', article=article)

# borrar articulos
@root.route('/delete', methods=['GET','POST'])
def delete():
    if request.method=='POST':
        ex=request.form.getlist('ext')
        delete_article(ex)
        return redirect(url_for('root.delete'))
    search_query = request.args.get('query','')
    if search_query:
        frontquery=search_blog(get_article)
    else:
        frontquery=blogquery()
    return render_template('blog/delete.html', frontquery=frontquery)

@root.route('/insert')
def insert():
    return render_template('blog/insert.html')