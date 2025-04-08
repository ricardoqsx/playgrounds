import sqlite3

# establece la conexion
blog = 'blog.db'
def gcon():
    return sqlite3.connect(blog)

# Consulta para hacer la presentacion de los articulos en el index
def posts(pagina=1, por_pagina=8):
    offset = (pagina - 1) * por_pagina
    with gcon() as con:
        cur = con.cursor()
        # Agregamos LIMIT y OFFSET
        sql = """
            SELECT id, titulo, substr(historia, 1, 300) || '...' as preview 
            FROM blog
            LIMIT ? OFFSET ?
        """
        cur.execute(sql, (por_pagina, offset))
        return cur.fetchall()
    
# obtener el total de articulos
def total_articulos():
    with gcon() as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM blog")
        return cur.fetchone()[0]
    
# lectura de articulos para la ruta dinamica
def read_article(article_id):
    with gcon() as con:
        cur = con.cursor()
        cur.execute("SELECT id, titulo, categoria, autor, historia FROM blog WHERE id = ?", (article_id,))
        article = cur.fetchone()
    return article