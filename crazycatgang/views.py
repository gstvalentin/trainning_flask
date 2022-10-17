from distutils.command.config import config
from flask import flash, render_template, request, redirect, session, url_for, send_from_directory
from app import app, db
from models import Gatos, Usuarios
from helpers import recupera_img


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
    
    arquivo = request.files['arquivo']
    uploads_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{uploads_path}/Foto_{novo_gato.id}.jpg')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

#! -------------------- PUT METHOD --------------------- EDITAR PARA FICAR PUT METHOD

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    gato = Gatos.query.filter_by(id=id).first()
    titulo = f'Você está editando os dados do seguinte gatinho: {gato.nome.capitalize()}'
    foto_gato = recupera_img(id)
    return render_template('editar.html', titulo=titulo, gato=gato, foto_gato=foto_gato)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    gato = Gatos.query.filter_by(id=request.form['id']).first()
    gato.nome = request.form['nome']
    gato.idade = request.form['idade']
    gato.castracao = request.form['castracao']
    db.session.add(gato)
    db.session.commit()
    
    arquivo = request.files['arquivo']
    uploads_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{uploads_path}/Foto_{gato.id}.jpg')
    
    return redirect(url_for('index'))

#! ------------------ DELETE METHOD ----------------------- USAR DELETE METHOD

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    gato = Gatos.query.filter_by(id=id).first()
    flash(f'Cadastro do gato {gato.nome.capitalize()} foi deletado!')
    Gatos.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('index'))



# -------------------- USER LOGIN ------------------
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
# -------------------- END USER LOGIN ---------------

@app.route('/<name>') #404
def print_name(name):
    return render_template('404.html')

