from flask import render_template, request, redirect, url_for, Blueprint
from app.models.blog_db import *

create_blog()

admin = Blueprint('admin',__name__, url_prefix='/admin')

# ==== inicio ===
@admin.route('/')
def home():
    search_query = request.args.get('query', '') 
    if search_query:
        frontblog = search_blog(search_query)
    else:
        frontblog = blogquery()
    return render_template('admin/home.html', frontblog=frontblog)

# Ruta dinamica para visualizar articulos
@admin.route('/<int:article_id>')
def view_story(article_id):
    # Obtenemos los datos del artículo
    article = get_article(article_id)
    if not article:
        return render_template('admin/404.html'), 404
    # Se pasa el artículo a la plantilla con el nombre 'article'
    return render_template('admin/article.html', article=article)

# ==== editar articulos // listar articulos ===
@admin.route('/insert', methods=['GET','POST'])
def insert():
    if request.method == 'POST':
        # recibe datos del formulario
        titul = request.form['titulo']
        categ = request.form['categoria']
        autor = request.form['autor']
        content = request.form['contenido']
        create_article(titul, categ, autor, content)
        return redirect(url_for('admin.insert'))
    return render_template('admin/insert.html')

# ==== editar articulos // vista ampliada ===
@admin.route('/edit')
def edit():
    search_query = request.args.get('query', '') 
    if search_query:
        frontblog = search_blog(search_query)
    else:
        frontblog = blogquery()
    return render_template('admin/edit.html', frontblog=frontblog)

# Ruta dinamica para editar articulos de manera individual
@admin.route('/edit/<int:article_id>', methods=['GET','POST'])
def edit_story(article_id):
    article = get_article(article_id)
    if not article:
        return render_template('admin/404.html'), 404
    if request.method == 'POST':
        new_id = request.form['ids']
        new_title = request.form['titulo']
        new_category = request.form['categoria']
        new_autor = request.form['autor']
        new_content = request.form['contenido']
        update_article(new_id, new_title, new_category, new_autor, new_content)
        return redirect(url_for('admin.edit_story', article_id=article_id))
    return render_template('admin/edit_full.html', article=article)

# ==== borrar articulos ===
@admin.route('/delete', methods=['GET','POST'])
def delete():
    if request.method=='POST':
        ex=request.form.getlist('ext')
        delete_article(ex)
        return redirect(url_for('admin.delete'))
    search_query = request.args.get('query','')
    if search_query:
        frontquery=search_blog(get_article)
    else:
        frontquery=blogquery()
    return render_template('admin/delete.html', frontquery=frontquery)