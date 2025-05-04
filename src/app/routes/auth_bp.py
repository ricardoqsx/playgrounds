from flask import render_template, request, Blueprint, redirect, url_for, flash
from app.models.users import *
from flask_login import login_user, logout_user

create_users()

auth = Blueprint('auth',__name__,url_prefix='/auth')

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash("Completa todos los campos")
            return render_template('auth/login.html')
        
        # Buscar usuario en BD
        logged_user = ModelUser.login(username, password)
        if logged_user:
            login_user(logged_user)
            return redirect(url_for('admin.home'))
        else:
            flash("Usuario o contraseña incorrectos")
            return render_template('auth/login.html')
    return render_template('auth/login.html')

@auth.route('/registro', methods=['GET', 'POST'])
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
    
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def status_404(error):
    return render_template('utils/404.html'), 404

def status_401(error):
    return render_template('utils/401.html'), 401