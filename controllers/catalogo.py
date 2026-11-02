from flask import Blueprint,render_template,request,redirect,session
from models import produto,cliente
bp=Blueprint('catalogo',__name__)
@bp.route('/home')
def home():
    if 'uid' not in session:return redirect('/')
    return render_template('home.html',itens=produto.destaques())
@bp.route('/produtos')
def produtos():
    if 'uid' not in session:return redirect('/')
    f=request.args.get('f','')
    return render_template('produtos.html',itens=produto.listar(f),f=f)
@bp.route('/perfil')
def perfil():
    if 'uid' not in session:return redirect('/')
    return render_template('perfil.html',u=cliente.buscar(session['uid']))
