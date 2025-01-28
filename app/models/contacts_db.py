import sqlite3
import pandas as pd

contacts_db = 'contacts.db'

def get_conn():
    return sqlite3.connect(contacts_db)

def create_db():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute(''' 
            create table if not exists contacts(
            ext integer primary key, 
            user text not null,
            mail text not null,
            phone text not null,
            site text not null,
            department text not null)''')
        cur.execute("select count(*) from contacts")
        res=cur.fetchone()
        if res is not None:
            if res[0]==0:
                df = pd.read_csv('agenda.csv')
                columns_to_insert = [ 'ext', 'user', 'mail', 'phone', 'site', 'department']
                df.to_sql('contacts', con, if_exists='append', index=False)

def query():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("Select * from contacts order by user asc")
        total = cur.fetchall()
    return total

def search_data(val):
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("select * from contacts where user like ?",('%'+val+'%',))
        total = cur.fetchall()
    return total

def dep_data():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("select departments from contacts")
        total = cur.fetchall()
    return total

def create_data(ex,us,ma,ph,st,dp):
    with get_conn() as con:
        cur = con.cursor()
        inser_data= "insert into contacts (ext, user, mail, phone, site, department) values (?, ?, ?, ?, ?, ?)"
        cur.execute(inser_data,(ex, us, ma, ph, st, dp))

def update_data(us, ma, ph, st, dp, ex):
    with get_conn() as con:
        cur = con.cursor()
        upd = ''' update contacts 
                    set user =?, 
                    mail = ?, 
                    phone = ?,
                    site = ?,
                    department = ? 
                  where ext = ?
              '''
        cur.execute(upd,(us, ma, ph, st, dp, ex))

def delete_data(ex):
    with get_conn() as con:
        cur = con.cursor()
        for ext in ex:
            cur.execute("delete from contacts where ext = ?", (ext,))