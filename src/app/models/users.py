from werkzeug.security import check_password_hash, generate_password_hash
import re
from flask_login import UserMixin
from app.models.db import get_conn


def create_users():
    with get_conn() as connect:
        cursor = connect.cursor()
        cursor.execute('''
            create table if not exists `user`(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       username VARCHAR(100) NOT NULL UNIQUE,
                       password VARCHAR(255) NOT NULL,
                       fullname VARCHAR(150) NOT NULL,
                       mail VARCHAR(255) NOT NULL UNIQUE,
                       institution VARCHAR(150),
                       charge VARCHAR(150))''')
        cursor.execute("select count(*) from `user`")
        result = cursor.fetchone()
        if result[0] == 0:
            prova_user = ("insert into `user`(username, password, fullname, mail, institution, charge) values (%s, %s, %s, %s, %s, %s)")
            usr = "admin"
            passwd = generate_password_hash("qwerty123")
            fullnm = "Administrator"
            ml = "jason_ing@live.com"
            insti = "UTP"
            chrg = "System Administrator"
            cursor.execute(prova_user,(usr, passwd, fullnm, ml, insti, chrg))

class User(UserMixin):
    def __init__(self, id, username, password, fullname="", mail="", institution="", charge="") -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.mail = mail
        self.institution = institution
        self.charge = charge

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

# Model user es para verificar si un usuario existe    
class ModelUser:
    @classmethod
    def login(cls, username, password):
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, password, fullname FROM `user` WHERE username = %s",
                (username,)
            )
            user_data = cursor.fetchone()
            if user_data:
                user_id, db_username, db_password, fullname = user_data
                if check_password_hash(db_password, password):
                    return User(user_id, db_username, db_password, fullname)
            return None
   
    @classmethod
    def get_by_id(self, id):
        with get_conn() as connect:
            cursor = connect.cursor()
            sql = "SELECT id, username, password, fullname FROM `user` WHERE id = %s"
            cursor.execute(sql, (int(id),))  # Convertir a entero
            result = cursor.fetchone()
            if result:
                return User(result[0], result[1], result[2], result[3])
            return None

#  esta es para ver el listado total de usuarios, omitiendo la contraseña        
def view_users():
    with get_conn() as connect:
        cursor = connect.cursor()
        cursor.execute("select id, username, fullname, mail, institution, charge, creation from `user`")
        return cursor.fetchall()

def edit_users(user_id):
    with get_conn() as connect:
        cursor = connect.cursor()
        cursor.execute("select id, username, fullname, mail, institution, charge, creation from `user` where id = %s", (user_id,))
        userid= cursor.fetchone()
        return userid

# verificar si un usuario o correos ya existen en la BD
def user_exists(uname, mail):
    with get_conn() as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT 1 FROM `user` WHERE username = %s OR mail = %s", (uname, mail))
        return cursor.fetchone() is not None                 

# verificar si el correo es valido
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# validar si la contraseña es fuerte
def is_strong_password(password):
    # Mínimo 8 caracteres, al menos 1 mayúscula, 1 número, y 1 especial
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*()_+]", password):
        return False
    return True

def insert_user(uname, passwd,fname,mail,insti,charge):
    with get_conn() as connect:
        cursor = connect.cursor()
        hash_passwd = generate_password_hash(passwd)
        cursor.execute('''
            INSERT INTO `user` 
            (username, password, fullname, mail, institution, charge)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (uname, hash_passwd, fname, mail, insti, charge))
    
def delete_user(ex):
    with get_conn() as con:
        cur = con.cursor()
        for ext in ex:
            cur.execute("delete from `user` where id = %s", (ext,))
