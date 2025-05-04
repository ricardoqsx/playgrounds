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

@users.route('/registro', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        fullname = request.form['fullname']
        institution = request.form.get('institution', '')
        charge = request.form.get('charge', '')
        # Validaciones secuenciales (detienen el flujo si fallan)
        if user_exists(username, email):
            flash("⚠️ El usuario o correo ya están registrados", "error")
            return render_template('users/register.html', form_data=request.form)
        if not is_valid_email(email):
            flash("⚠️ Formato de correo electrónico inválido", "error")
            return render_template('users/register.html', form_data=request.form)
        if not is_strong_password(password):
            flash("🔒 La contraseña debe tener 8+ caracteres, mayúsculas, números y símbolos", "error")
            return render_template('users/register.html', form_data=request.form)
        # Si pasa todas las validaciones, crear usuario
        insert_user(username, password, fullname, email, institution, charge)
        flash("✅ Usuario creado exitosamente", "success")
        return redirect(url_for('auth.login'))
    return render_template('users/register.html')

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