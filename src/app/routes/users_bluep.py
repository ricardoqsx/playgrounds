from flask import Blueprint, render_template

users = Blueprint('users',__name__,url_prefix='/users')

@users.route('/')
def inicio():
    return render_template('users/index.html')