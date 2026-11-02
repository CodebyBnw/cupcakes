import uuid
from database import get_db
import re
def cep_valido(cep):
    return bool(re.fullmatch(r'\d{5}-?\d{3}',cep or ''))
def calcular_frete(cep,subtotal):
    if not cep_valido(cep):return 0
    return 0 if cep.startswith('80') and subtotal>=50 else 8
def criar(cliente_id,cart,forma,frete):
    db=get_db();total=sum(i['qt']*i['unit'] for i in cart)+frete;cod=uuid.uuid4().hex[:8].upper()
    cur=db.execute('insert into pedido(codigo,cliente_id,status,forma_pgto,valor_total,frete) values(?,?,?,?,?,?)',(cod,cliente_id,'Aprovado',forma,total,frete))
    for i in cart:
        db.execute('insert into item_pedido(pedido_id,produto_id,quantidade,massa,recheio,subtotal) values(?,?,?,?,?,?)',(cur.lastrowid,i['pid'],i['qt'],i['massa'],i['recheio'],i['qt']*i['unit']))
        db.execute('update produto set estoque=estoque-? where id=?',(i['qt'],i['pid']))
    db.commit();return cod,total
def do_cliente(cid):
    return get_db().execute('select * from pedido where cliente_id=? order by id desc',(cid,)).fetchall()
def itens(pid):
    return get_db().execute('select i.*,p.nome from item_pedido i join produto p on p.id=i.produto_id where pedido_id=?',(pid,)).fetchall()
def fila():
    return get_db().execute("select * from pedido where status in('Aprovado','Em Preparacao') order by data_hora").fetchall()
def mudar_status(pid,st):
    if st in('Em Preparacao','Pronto'):
        get_db().execute('update pedido set status=? where id=?',(st,pid));get_db().commit()
