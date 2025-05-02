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
    
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def status_404(error):
    return render_template('utils/404.html'), 404

def status_401(error):
    return render_template('utils/401.html'), 401