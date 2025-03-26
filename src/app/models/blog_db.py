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
                    id integer,
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

def blogquery():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("select id, titulo, categoria, autor from blog order by id asc")
        total = cur.fetchall()
    return total

def search_blog(val):
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("select * from blog where titulo like ?",('%'+val+'%',))
        total = cur.fetchall()
    return total

def list_ids(ids):
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("select id from blog where id = '?', (ids,)")
        ids = cur.fetchone()
        return ids