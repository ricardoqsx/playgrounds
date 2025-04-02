import os
import sqlite3
import pandas as pd

blog = 'contacts.db'

def get_conn():
    return sqlite3.connect(blog)

def create_blog():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute('''
            create table if not exists blog(
                    id integer primary key autoincrement,
                    titulo text not null,
                    categoria text not null,
                    autor text not null,
                    historia text not null)''')
        cur.execute("select count(*) from blog")
        res=cur.fetchone()
        if res is not None:
            if res[0]==0:
                current_dir = os.path.dirname(__file__)
                csv_path = os.path.join(current_dir, "blog.csv")
                df = pd.read_csv(csv_path)
                columns_to_insert = ['id','titulo','categoria','autor','historia']
                df.to_sql('blog', con, if_exists='append', index=False)

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
        cur.execute("select * from blog where titulo like ?",('%'+val+'%',))
        total = cur.fetchall()
    return total

#Consulta para la ruta dinamica
def get_article(article_id):
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("SELECT id, titulo, categoria, autor, historia FROM blog WHERE id = ?", (article_id,))
        article = cur.fetchone()
        return article

# Consulta para crear articulo
def create_article(ex,us,ma,ph):
    with get_conn() as con:
        cur = con.cursor()
        inser_data= "insert into blog (titulo, categoria, autor, historia) values (?, ?, ?, ?)"
        cur.execute(inser_data,(ex, us, ma, ph))

# Consulta para editar articulos
def update_article(ids, titulo, categ, aut, stor):
    with get_conn() as con:
        cur = con.cursor()
        upd = ''' update blog 
                    set titulo =?, 
                    categoria = ?, 
                    autor = ?,
                    historia = ?
                  where id = ?
              '''
        cur.execute(upd,(titulo, categ, aut, stor, ids))

# Consulta para borrar articulos
def delete_article(ex):
    with get_conn() as con:
        cur = con.cursor()
        for ext in ex:
            cur.execute("delete from blog where id = ?", (ext,))