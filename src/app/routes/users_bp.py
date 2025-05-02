from flask import Blueprint, render_template
from app.models.users import view_users

users = Blueprint('users',__name__,url_prefix='/users')

@users.route('/')
def inicio():
    users = view_users()
    return render_template('users/index.html', users=users)