from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_login import login_required
from app.models.contacts_db import contacts_db

agenda_bp = Blueprint('crud',__name__)

@agenda_bp.route('/')
def index():
    query = request.args.get('query','')
    if query:
        frontquery=contacts_db.search_data(query)
    else:
        frontquery=contacts_db.query()
    return render_template('index.html', frontquery=frontquery)

@agenda_bp.route('/insert', methods=['GET', 'POST'])
@login_required
def insert():
    if request.method == 'POST':
        # recibe datos del formulario
        ext = request.form['ext']
        user = request.form['user']
        mail = request.form['mail']
        phone = request.form['phone']
        site = request.form['site']
        department = request.form['department']
        db.create_data(ext, user, mail, phone, site, department)
        return redirect(url_for('insert'))
    frontquery=contacts_db.query()
    return render_template('admin/insert.html', frontquery=frontquery)

@agenda_bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        selected_exts = request.form.getlist('ext')
        for ext in selected_exts:
            user = request.form.get(f'user_{ext}')
            mail = request.form.get(f'mail_{ext}')
            phone = request.form.get(f'phone_{ext}')
            site = request.form.get(f'site_{ext}')
            department = request.form.get(f'department_{ext}')
            contacts_db.update_data(user, mail, phone, site, department, ext)
        return redirect(url_for('update'))

    query = request.args.get('query', '')
    frontquery = contacts_db.search_data(query) if query else contacts_db.query()
    return render_template('admin/update.html', frontquery=frontquery)

@agenda_bp.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method=='POST':
        ex=request.form.getlist('ext')
        contacts_db.delete_data(ex)
        return redirect(url_for('delete'))
    query = request.args.get('query','')
    if query:
        frontquery=contacts_db.search_data(query)
    else:
        frontquery=contacts_db.query()
    return render_template('admin/delete.html', frontquery=frontquery)