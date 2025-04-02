from flask import render_template, request, redirect, url_for, Blueprint

home = Blueprint('home',__name__)

@home.route('/')
def index():
    return render_template('index.html')