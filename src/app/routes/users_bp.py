from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from app.models.users import *


users = Blueprint('users',__name__,url_prefix='/users')

@users.before_request
def check_authenticated():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

@users.route('/')
def inicio():
    users = view_users()
    return render_template('users/index.html', users=users)

@users.route('/edit/<int:user_id>')
def edit(user_id):
    users = edit_users(user_id)
    if not users:
        return render_template('admin/404.html'), 404
    return render_template('users/edit.html', users=users)

# ==== borrar usuarios ===
@users.route('/delete', methods=['GET','POST'])
def delete():
    if request.method=='POST':
        ex=request.form.getlist('ext')
        delete_user(ex)
        return redirect(url_for('users.delete'))
    else:
        frontquery=view_users()
    return render_template('users/delete.html', frontquery=frontquery)