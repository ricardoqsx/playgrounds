from werkzeug.security import check_password_hash #, generate_password_hash
import sqlite3

class User():
    def __init__(self, id, username, password, fullname="")-> None:
        self.id=id
        self.username=username
        self.password=password
        self.fullname=fullname

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
    
# print(generate_password_hash("qwerty123"))

users = 'user.db'
def users_connect():
    return sqlite3.connect(users)

def create_users():
    with users_connect() as connect:
        cursor = connect.cursor()
        cursor.execute('''
            create table if not exists user(
                       id integer primary key autoincrement,
                       username text,
                       password text,
                       fullname text)''')
        cursor.execute("select count(*) from user")
        result = cursor.fetchone()
        if result is not None:
            prova_user = ("insert into user(username, password, fullname) values (?, ?, ?)")
            usr = "test"
            passwd = "scrypt:32768:8:1$hV1bmtqJ1iPnMPQe$32b7ec324c0800145b346c0b55ab8a1f1deb661cdf9d616c293c3011eec6ee7068b3ff8733ecc303c805ad8d6be194dbad622911af1b1a95ae2d1583b7286a63"
            cursor.execute(prova_user,(usr, passwd, "Test User"))
    
class ModelUser():
    @classmethod
    def login(self,user):
        with users_connect() as connect:
            cursor = connect.cursor()
            sql = "select id, username, password, fullname from user where username = ?"
            cursor.execute(sql,(user.username,))
            result = cursor.fetchone()
            if result is not None:
                if User.check_password(result[2],user.password):
                    return User(result[0],result[1],result[2],result[3])
            else:
                return None
                 


