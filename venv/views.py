from flask import flash, render_template, request, redirect, session, url_for
from app import app, db
from models import Gatos, Usuarios


@app.route('/')
def index():
    lista = Gatos.query.order_by(Gatos.id)
    return render_template('lista.html', titulo='Crazy Cat Gang', gatos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome  = request.form['nome']
    idade = request.form['idade']
    castracao = request.form['castracao']
    
    gato = Gatos.query.filter_by(nome=nome).first() #True or False | se já existe gato com mesmo nome
    if gato:
        flash(f'Gato já adicionado na base de dados')
        return redirect(url_for('index'))
    
    novo_gato = Gatos(nome=nome, idade=idade, castracao=castracao) #guarda os inputs
    db.session.add(novo_gato) #add os inputs
    db.session.commit() # commit e leva para db
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first() #True or False | input user do campo usuario login.html
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(f'Usuário {usuario.nickname} Logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout Efetuado com sucesso!')
    return redirect(url_for('index'))
    

@app.route('/<name>') #404
def print_name(name):
    return render_template('404.html')