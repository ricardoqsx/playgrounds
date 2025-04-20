from flask import Blueprint, render_template

pruebas = Blueprint('pruebas',__name__,url_prefix='/pruebas')

@pruebas.route('/test')
def test():
    return render_template('blog/test.html')