from flask import render_template, request, redirect, url_for, Blueprint
# from models.contacts_db import contacts_db

agenda = Blueprint('agenda',__name__, url_prefix='/admin')

@agenda.route('/index')
def index():
    return render_template('index.html')

@agenda.route('/insert', methods=['GET'])
def insert():
    return render_template('admin/insert.html')

@agenda.route('/update', methods=['GET'])
def update():
    return render_template('admin/update.html')

@agenda.route('/delete', methods=['GET'])
def delete():
    return render_template('admin/delete.html')









"""
@agenda.route('/delete', methods=['GET', 'POST'])
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
@agenda.route('/')
def index():
    query = request.args.get('query','')
    if query:
        frontquery=contacts_db.search_data(query)
    else:
        frontquery=contacts_db.query()
    return render_template('index.html', frontquery=frontquery)

@agenda.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        # recibe datos del formulario
        ext = request.form['ext']
        user = request.form['user']
        mail = request.form['mail']
        phone = request.form['phone']
        site = request.form['site']
        department = request.form['department']
        contacts_db.create_data(ext, user, mail, phone, site, department)
        return redirect(url_for('insert'))
    frontquery=contacts_db.query()
    return render_template('admin/insert.html', frontquery=frontquery)

@agenda.route('/update', methods=['GET', 'POST'])
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

@agenda.route('/delete', methods=['GET', 'POST'])
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
    
    """