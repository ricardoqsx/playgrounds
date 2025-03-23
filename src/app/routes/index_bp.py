from flask import render_template, request, redirect, url_for, Blueprint
from app.models.contacts_db import query, search_data

index = Blueprint('index',__name__)

@index.route('/')
def home():
    search_query = request.args.get('query', '') 
    if search_query:
        frontq = search_data(search_query)
    else:
        frontq = query()
    return render_template('index.html', frontq=frontq)

@index.route('/inicio')
def inicio():
    return render_template('home/home.html')