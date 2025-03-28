from flask import render_template, request, redirect, url_for, Blueprint
from app.models.agenda_db import search_data,query
from app.models.blog_db import *

create_blog()

root = Blueprint('root',__name__)

@root.route('/')
def home():
    search_query = request.args.get('query', '') 
    if search_query:
        frontblog = search_blog(search_query)
    else:
        frontblog = blogquery()
    return render_template('blog/home.html', frontblog=frontblog)

@root.route('/home/<int:ids>')
def view_story(ids):
    ids= list_ids(ids)
    if not ids:
        return "articulo no encontrado", 404
    return render_template('blog/list_stories.html',ids=ids)