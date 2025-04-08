from flask import render_template, request, redirect, url_for, Blueprint, flash
from app.models.admin_db import *
from app.models.users import *
from flask_login import LoginManager, login_user, logout_user, login_required

create_blog()
create_users()

admin = Blueprint('admin',__name__, url_prefix='/admin')

#@login_manager_app.user_loader
#def load_user(id):
#    return ModelUser.get_by_id(id)

# ==== inicio ===
@admin.route('/')
def home():
    search_query = request.args.get('query', '') 
    if search_query:
        frontblog = search_blog(search_query)
    else:
        frontblog = blogquery()
    return render_template('admin/home.html', frontblog=frontblog)

@admin.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User(0,request.form['username'],request.form['password'])
        logged_user = ModelUser.login(user)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('admin.home'))
            else:
                flash("Contraseña Invalida...")
                return render_template('admin/login.html')
        else:
            flash("Usuario no encontrado...")
            return render_template('admin/login.html')
    else:
        return render_template('admin/login.html')

# Ruta dinamica para visualizar articulos
@admin.route('/<int:article_id>')
#@login_required
def view_story(article_id):
    # Obtenemos los datos del artículo
    article = get_article(article_id)
    if not article:
        return render_template('admin/404.html'), 404
    # Se pasa el artículo a la plantilla con el nombre 'article'
    return render_template('admin/article.html', article=article)

# ==== editar articulos // listar articulos ===
@admin.route('/insert', methods=['GET','POST'])
#@login_required
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
#@login_required
def edit():
    search_query = request.args.get('query', '') 
    if search_query:
        frontblog = search_blog(search_query)
    else:
        frontblog = blogquery()
    return render_template('admin/edit.html', frontblog=frontblog)

# Ruta dinamica para editar articulos de manera individual
@admin.route('/edit/<int:article_id>', methods=['GET','POST'])
#@login_required
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
#@login_required
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