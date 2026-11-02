import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
from database import get_db
def criar(nome,telefone,email,senha):
    try:
        get_db().execute('insert into cliente(nome,telefone,email,senha) values(?,?,?,?)',(nome,telefone,email.strip().lower(),generate_password_hash(senha)))
        get_db().commit();return True
    except sqlite3.IntegrityError:return False
def autenticar(email,senha):
    u=get_db().execute('select * from cliente where email=?',(email.strip().lower(),)).fetchone()
    return u if u and check_password_hash(u['senha'],senha) else None
def buscar(cid):
    return get_db().execute('select * from cliente where id=?',(cid,)).fetchone()
