from database import get_db
def listar(filtro=''):
    q='select p.*,c.restricao from produto p join categoria c on c.id=p.categoria_id';a=()
    if filtro in('sem gluten','sem lactose'):q+=' where c.restricao=?';a=(filtro,)
    return get_db().execute(q,a).fetchall()
def destaques(n=4):
    return get_db().execute('select * from produto where estoque>0 limit ?',(n,)).fetchall()
def buscar(pid):
    return get_db().execute('select * from produto where id=?',(pid,)).fetchone()
