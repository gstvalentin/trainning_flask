from flask import Flask, flash, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'miau'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'root',
        servidor = 'localhost',
        database = 'catgang'
    )

db = SQLAlchemy(app)

class Gatos(db.Model):
    id = db.Column(db.Integer, primary_key= True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.String(2), nullable=False)
    castracao = db.Column(db.String(5), nullable=False)
    
    def __repr__(self) -> str:
        return '<Name %r>' % self.name

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key= True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    
    def __repr__(self) -> str:
        return '<Name %r>' % self.name


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

# trecho da app
app.run(host='0.0.0.0', port=8080, debug=True)