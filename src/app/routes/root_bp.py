from flask import render_template, request, redirect, url_for, Blueprint
from app.models.agenda_db import search_data,query
from app.models.blog_db import *

create_blog()

root = Blueprint('root',__name__)

@root.route('/')
def index():
    search_query = request.args.get('query', '') 
    if search_query:
        frontq = search_data(search_query)
    else:
        frontq = query()
    return render_template('index.html', frontq=frontq)

@root.route('/inicio')
def home():
    search_query = request.args.get('query', '') 
    if search_query:
        frontblog = search_blog(search_query)
    else:
        frontblog = blogquery()
    return render_template('home/home.html', frontblog=frontblog)