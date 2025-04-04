import sqlite3

# establece la conexion
blog = 'blog.db'
def gcon():
    return sqlite3.connect(blog)

# Consulta para hacer la presentacion de los articulos en el index
def posts():
    with gcon() as con:
        cur = con.cursor()
        post = "select id, titulo, substr(historia, 1, 300) || '...' as preview from blog"
        cur.execute(post)
        resultados = cur.fetchall()
        return resultados
    
# lectura de articulos para la ruta dinamica
def read_article(article_id):
    with gcon() as con:
        cur = con.cursor()
        cur.execute("SELECT id, titulo, categoria, autor, historia FROM blog WHERE id = ?", (article_id,))
        article = cur.fetchone()
    return article