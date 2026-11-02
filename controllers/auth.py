from flask import Blueprint,render_template,request,redirect,session,flash
from models import cliente
bp=Blueprint('auth',__name__)
@bp.route('/',methods=['GET','POST'])
def login():
    if request.method=='POST':
        u=cliente.autenticar(request.form['email'],request.form['senha'])
        if u:
            session['uid']=u['id'];session['nome']=u['nome'];return redirect('/home')
        flash('Email ou senha invalidos')
    return render_template('login.html')
@bp.route('/cadastro',methods=['GET','POST'])
def cadastro():
    if request.method=='POST':
        f=request.form
        if len(f['senha'])<6:
            flash('A senha deve ter no minimo 6 caracteres');return render_template('cadastro.html')
        if cliente.criar(f['nome'],f['telefone'],f['email'],f['senha']):return redirect('/')
        flash('Email ja cadastrado')
    return render_template('cadastro.html')
@bp.route('/sair')
def sair():
    session.clear();return redirect('/')
