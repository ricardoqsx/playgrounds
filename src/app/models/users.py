from werkzeug.security import check_password_hash, generate_password_hash
import re
import sqlite3
from flask_login import UserMixin

# creacion de la bd e insercion de un usuario para pruebas
users = 'user.db'
def users_connect():
    return sqlite3.connect(users)

def create_users():
    with users_connect() as connect:
        cursor = connect.cursor()
        cursor.execute('''
            create table if not exists user(
                       id integer primary key autoincrement,
                       creation timestamp default (datetime('now', 'localtime')),
                       username text not null unique,
                       password text not null,
                       fullname text not null,
                       mail text not null unique,
                       institution text,
                       charge text)''')
        cursor.execute("select count(*) from user")
        result = cursor.fetchone()
        if result[0] == 0:
            prova_user = ("insert into user(username, password, fullname, mail, institution, charge) values (?, ?, ?, ?, ?, ?)")
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
        with users_connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, password, fullname FROM user WHERE username = ?",
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
        with users_connect() as connect:
            cursor = connect.cursor()
            sql = "SELECT id, username, password, fullname FROM user WHERE id = ?"
            cursor.execute(sql, (int(id),))  # Convertir a entero
            result = cursor.fetchone()
            if result:
                return User(result[0], result[1], result[2], result[3])
            return None
        
def view_users():
    with users_connect() as connect:
        cursor = connect.cursor()
        cursor.execute("select username, fullname, mail, institution, charge, creation from user")
        return cursor.fetchall()

def user_exists(uname, mail):
    with users_connect() as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT 1 FROM user WHERE username = ? OR mail = ?", (uname, mail))
        return cursor.fetchone() is not None                 

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

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

def insert_user(uname, passwd, fname, mail, insti, charge):
    # Validaciones secuenciales con mensajes específicos
    if user_exists(uname, mail):
        raise ValueError("El nombre de usuario o correo electrónico ya está registrado")
    
    if not is_valid_email(mail):
        raise ValueError("Formato de correo electrónico inválido")
    
    if not is_strong_password(passwd):
        raise ValueError(
            "La contraseña debe contener:\n"
            "- Mínimo 8 caracteres\n"
            "- Al menos una mayúscula\n"
            "- Al menos un número\n"
            "- Al menos un carácter especial"
        )
    
    try:
        with users_connect() as connect:
            cursor = connect.cursor()
            hash_passwd = generate_password_hash(passwd)
            
            # Validación adicional del hash
            if not hash_passwd:
                raise RuntimeError("Error al generar el hash de la contraseña")
            
            cursor.execute('''
                INSERT INTO user 
                (username, password, fullname, mail, institution, charge)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (uname, hash_passwd, fname, mail, insti, charge))
            
            # Verificación de inserción exitosa
            if cursor.rowcount != 1:
                raise RuntimeError("No se pudo crear el usuario")
            
            return True  # Indicador de éxito
            
    except sqlite3.IntegrityError as e:
        # Captura violaciones de UNIQUE que podrían ocurrir por race conditions
        connect.rollback()
        raise ValueError("El usuario o correo ya existe (error de base de datos)") from e
        
    except sqlite3.Error as e:
        connect.rollback()
        raise RuntimeError(f"Error de base de datos: {str(e)}") from e
        
    except Exception as e:
        connect.rollback()
        raise RuntimeError(f"Error inesperado: {str(e)}") from e