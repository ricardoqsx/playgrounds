import os
import pandas as pd
from app.models.db import get_conn


def create_blog():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS blog(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    titulo VARCHAR(255) NOT NULL,
                    categoria VARCHAR(100) NOT NULL,
                    autor VARCHAR(150) NOT NULL,
                    historia LONGTEXT NOT NULL)''')
        cur.execute("select count(*) from blog")
        res=cur.fetchone()
        if res is not None:
            if res[0]==0:
                current_dir = os.path.dirname(__file__)
                csv_path = os.path.join(current_dir, "blog.csv")
                df = pd.read_csv(csv_path)
                insert_data = "insert into blog (id, titulo, categoria, autor, historia) values (%s, %s, %s, %s, %s)"
                cur.executemany(insert_data, df[['id', 'titulo', 'categoria', 'autor', 'historia']].values.tolist())

# Consulta basica par mostrar la tabla
def blogquery():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("select id, titulo, categoria, autor from blog order by id asc")
        total = cur.fetchall()
    return total

# Consulta del campo de busqueda
def search_blog(val):
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("select * from blog where titulo like %s",('%'+val+'%',))
        total = cur.fetchall()
    return total

#Consulta para la ruta dinamica
def get_article(article_id):
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("SELECT id, titulo, categoria, autor, historia FROM blog WHERE id = %s", (article_id,))
        article = cur.fetchone()
    return article

# Consulta para crear articulo
def create_article(ex,us,ma,ph):
    with get_conn() as con:
        cur = con.cursor()
        inser_data= "insert into blog (titulo, categoria, autor, historia) values (%s, %s, %s, %s)"
        cur.execute(inser_data,(ex, us, ma, ph))

# Consulta para editar articulos
def update_article(ids, titulo, categ, aut, stor):
    with get_conn() as con:
        cur = con.cursor()
        upd = ''' update blog 
                    set titulo = %s, 
                    categoria = %s, 
                    autor = %s,
                    historia = %s
                  where id = %s
              '''
        cur.execute(upd,(titulo, categ, aut, stor, ids))

# Consulta para borrar articulos
def delete_article(ex):
    with get_conn() as con:
        cur = con.cursor()
        for ext in ex:
            cur.execute("delete from blog where id = %s", (ext,))
