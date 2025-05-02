from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from app.models.users import view_users


users = Blueprint('users',__name__,url_prefix='/users')

@users.before_request
def check_authenticated():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

@users.route('/')
def inicio():
    users = view_users()
    return render_template('users/index.html', users=users)