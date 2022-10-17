from flask import flash, render_template, request, redirect, session, url_for, send_from_directory, jsonify
from app import app, db
from models import Gatos, Usuarios
from helpers import recupera_img, deleta_arquivo
import time

@app.route('/')
def index():
    lista = Gatos.query.order_by(Gatos.id)
    return render_template('lista.html', titulo='Crazy Cat Gang', gatos=lista)

@app.route('/novo') #leva pra rota de cadastro
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None: #valida se usuario está logado e mantem rota após login
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Cadastro')

# ---------------- POST METHOD ---------------------

@app.route('/criar', methods=['POST',]) #pegando dados e iserindo da db
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
    timestamp = time.time()
    arquivo.save(f'{uploads_path}/Foto_{novo_gato.id}-{timestamp}.jpg')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

# -------------------- PUT METHOD --------------------- 

@app.route('/editar/<int:id>') #Valida login e apresenta edição de cadastro
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    gato = Gatos.query.filter_by(id=id).first()
    titulo = f'Você está editando os dados do seguinte gatinho: {gato.nome.capitalize()}'
    foto_gato = recupera_img(id)
    return render_template('editar.html', titulo=titulo, gato=gato, foto_gato=foto_gato)

@app.route('/atualizar', methods=['POST',]) #User consegue atualizar utilizando method POST
def atualizar():
    gato = Gatos.query.filter_by(id=request.form['id']).first()
    gato.nome = request.form['nome']
    gato.idade = request.form['idade']
    gato.castracao = request.form['castracao']
    
    db.session.add(gato)
    db.session.commit()
    
    arquivo = request.files['arquivo'] #request img do arquivo editar.html
    uploads_path = app.config['UPLOAD_PATH'] #path da pasta uploads
    timestamp = time.time() #secs para dar id unico para as imgs
    deleta_arquivo(gato.id) #deleta a img antiga antes de inserir a nova
    arquivo.save(f'{uploads_path}/Foto_{gato.id}-{timestamp}.jpg') #salva a nova img no path desejado
    
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['PUT',]) #? PUT method só utilizavel pelo postman
def atualiza_dados(id):
    gato = Gatos.query.filter_by(id=id).first()
    gato.nome = request.form['nome']
    gato.idade = request.form['idade']
    gato.castracao = request.form['castracao']
    
    db.session.add(gato)
    db.session.commit()
    
    return f'O gato {gato.nome} foi atualizado!'

# ------------------ DELETE METHOD -----------------------

@app.route('/deletar/<int:id>')# methods=['POST', 'DELETE']
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    # if request.method == 'DELETE':
    gato = Gatos.query.filter_by(id=id).first()
    flash(f'Cadastro do gato {gato.nome.capitalize()} foi deletado!')
    Gatos.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('index'))
    
@app.route('/delete/<int:id>', methods=['PUT','DELETE']) #? DELETE SÓ PELO POSTMAN
def deleta_gato(id):
    # if 'usuario_logado' not in session or session['usuario_logado'] == None: #!estudar como colocar autenticação direto na api
    #     return redirect(url_for('login')) 
    if request.method == 'DELETE':
        gato = Gatos.query.filter_by(id=id).first()
        db.session.delete(gato)
        db.session.commit()
        return f'Cadastro do gato {gato.nome.capitalize()} foi deletado!'


# --------------------- GET METHOD ----------------------
@app.route('/gatosapi', methods=['GET'])
def retorna_gatos():
    lista = Gatos.query.order_by(Gatos.id)
    api = []
    conteudo = {}
    for gato in lista:
        conteudo = {'id': gato.id, 'nome': gato.nome, 'idade': gato.idade, 'castracao': gato.castracao}
        api.append(conteudo)
        conteudo = {}
    return jsonify(api)


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

