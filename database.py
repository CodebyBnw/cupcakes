import sqlite3,os
BASE=os.path.dirname(os.path.abspath(__file__))
from flask import g
DB=os.path.join(BASE,'cupcakes.db')
def get_db():
    if 'db' not in g:
        g.db=sqlite3.connect(DB);g.db.row_factory=sqlite3.Row
    return g.db
def close_db(e=None):
    d=g.pop('db',None)
    if d:d.close()
def init_db():
    c=sqlite3.connect(DB);c.executescript(open(os.path.join(BASE,'schema.sql')).read())
    if not c.execute('select 1 from produto').fetchone():
        c.execute("insert into categoria(tipo,restricao) values('Classico','nenhuma'),('Sem gluten','sem gluten'),('Sem lactose','sem lactose')")
        c.executemany("insert into produto(categoria_id,nome,preco,ingredientes,estoque) values(?,?,?,?,?)",[(1,'Red Velvet',12,'Farinha, cacau, cream cheese',20),(1,'Choco Lover',14,'Chocolate, ganache',15),(2,'Baunilha SG',13,'Farinha de arroz, baunilha',10),(3,'Morango Vegano',15,'Morango, leite vegetal',0)])
        c.execute("insert into confeiteiro(nome,turno) values('Maria','Manha')")
    c.commit();c.close()
