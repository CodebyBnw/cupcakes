from flask import Blueprint,render_template,request,redirect,session,flash
from models import produto,pedido
bp=Blueprint('pedidos',__name__)
@bp.route('/add/<int:pid>',methods=['POST'])
def add(pid):
    p=produto.buscar(pid);qt=int(request.form.get('qt',1))
    cart=session.get('cart',[])
    ja=sum(i['qt'] for i in cart if i['pid']==pid)
    if not p or qt<1 or p['estoque']<qt+ja:
        flash('Produto esgotado ou quantidade indisponivel');return redirect('/produtos')
    extra=2.0 if request.form.get('premium') else 0
    cart.append({'pid':pid,'nome':p['nome'],'qt':qt,'unit':p['preco']+extra,'massa':request.form.get('massa','Baunilha'),'recheio':request.form.get('recheio','Brigadeiro')})
    session['cart']=cart;return redirect('/carrinho')
@bp.route('/carrinho')
def carrinho():
    if 'uid' not in session:return redirect('/')
    cart=session.get('cart',[]);sub=sum(i['qt']*i['unit'] for i in cart);cep=request.args.get('cep','')
    if cep and not pedido.cep_valido(cep):
        flash('CEP invalido. Use o formato 80000-000');cep=''
    return render_template('carrinho.html',cart=cart,sub=sub,cep=cep,frete=pedido.calcular_frete(cep,sub))
@bp.route('/remover/<int:i>')
def remover(i):
    cart=session.get('cart',[])
    if 0<=i<len(cart):cart.pop(i)
    session['cart']=cart;return redirect('/carrinho')
@bp.route('/checkout',methods=['POST'])
def checkout():
    cart=session.get('cart',[])
    if not cart:return redirect('/carrinho')
    cep=request.form.get('cep','')
    if not pedido.cep_valido(cep):
        flash('Informe um CEP valido');return redirect('/carrinho')
    forma=request.form['forma'];frete=pedido.calcular_frete(cep,sum(i['qt']*i['unit'] for i in cart))
    cod,total=pedido.criar(session['uid'],cart,forma,frete);session['cart']=[]
    return render_template('confirmacao.html',cod=cod,total=total,forma=forma)
@bp.route('/pedidos')
def meus():
    if 'uid' not in session:return redirect('/')
    return render_template('pedidos.html',ps=[{'p':p,'itens':pedido.itens(p['id'])} for p in pedido.do_cliente(session['uid'])])
@bp.route('/painel')
def painel():
    if 'uid' not in session:return redirect('/')
    return render_template('painel.html',ps=pedido.fila())
@bp.route('/painel/<int:i>/<st>')
def muda(i,st):
    if 'uid' not in session:return redirect('/')
    pedido.mudar_status(i,st);return redirect('/painel')
