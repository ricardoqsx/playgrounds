from app.models.db import get_conn


# //////////////// Vista completa de articulos ////////////////
# obtener el total de articulos
def total_articulos():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM blog")
        return cur.fetchone()[0]

# Consulta para hacer la presentacion de los articulos en el index
def posts(pagina=1, por_pagina=8):
    offset = (pagina - 1) * por_pagina
    with get_conn() as con:
        cur = con.cursor()
        # Agregamos LIMIT y OFFSET
        sql = """
            SELECT id, titulo, CONCAT(SUBSTRING(historia, 1, 300), '...') as preview 
            FROM blog
            LIMIT %s OFFSET %s
        """
        cur.execute(sql, (por_pagina, offset))
        return cur.fetchall()

# //////////////// Esto es para la busqueda! ////////////////
# Consulta del campo de busqueda
def total_articulos_busqueda(val):
    """Cuenta total de artículos que coinciden con la búsqueda"""
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("select count(*) from blog where titulo like %s", ('%'+val+'%',))
        return cur.fetchone()[0]

def buscar_posts(val, pagina=1, por_pagina=8):
    """Búsqueda paginada con LIMIT y OFFSET"""
    offset = (pagina - 1) * por_pagina
    with get_conn() as con:
        cur = con.cursor()
        sql = """
            select id, titulo, CONCAT(SUBSTRING(historia, 1, 300), '...') as preview 
            from blog 
            where titulo like %s
            limit %s offset %s
        """
        cur.execute(sql, ('%'+val+'%', por_pagina, offset))
        return cur.fetchall()
    
# //////////////// lectura de articulos para la ruta dinamica ////////////////
def read_article(article_id):
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("SELECT id, titulo, categoria, autor, historia FROM blog WHERE id = %s", (article_id,))
        article = cur.fetchone()
    return article
