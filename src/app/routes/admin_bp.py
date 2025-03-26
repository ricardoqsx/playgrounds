from flask import render_template, request, redirect, url_for, Blueprint
from app.models.agenda_db import *

admin = Blueprint('admin',__name__, url_prefix='/admin')

create_db()

@admin.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        # recibe datos del formulario
        ext = request.form['ext']
        user = request.form['user']
        mail = request.form['mail']
        phone = request.form['phone']
        site = request.form['site']
        department = request.form['department']
        create_data(ext, user, mail, phone, site, department)
        return redirect(url_for('admin.insert'))
    frontquery=query()
    return render_template('admin/insert.html', frontquery=frontquery)

@admin.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        selected_exts = request.form.getlist('ext')
        for ext in selected_exts:
            user = request.form.get(f'user_{ext}')
            mail = request.form.get(f'mail_{ext}')
            phone = request.form.get(f'phone_{ext}')
            site = request.form.get(f'site_{ext}')
            department = request.form.get(f'department_{ext}')
            update_data(user, mail, phone, site, department, ext)
        return redirect(url_for('admin.update'))

    search_query = request.args.get('query', '')
    frontquery = search_data(search_query) if query else query()
    return render_template('admin/update.html', frontquery=frontquery)

@admin.route('/delete', methods=['GET','POST'])
def delete():
    if request.method=='POST':
        ex=request.form.getlist('ext')
        delete_data(ex)
        return redirect(url_for('admin.delete'))
    search_query = request.args.get('query','')
    if search_query:
        frontquery=search_data(search_query)
    else:
        frontquery=query()
    return render_template('admin/delete.html', frontquery=frontquery) 
