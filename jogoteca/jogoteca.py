from flask import Flask, flash, render_template, request, redirect, session

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('Creu', 'Funk Pauleira', 'Radinho de pilha')
lista = [jogo1, jogo2]
    
app = Flask(__name__)
app.secret_key = 'creu'

@app.route('/')
def index():    
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome  = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if 'senha' == request.form['senha']: #name do campo de senha html
        nameuser = session['usuario_logado'] = request.form['usuario'] #name do campo usuario html
        flash(f'Usuário {nameuser} Logado com sucesso!')
        return redirect('/')
    else:
        flash('Usuário não logado')
        return redirect('/login')
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout Efetuado com sucesso!')
    return redirect('/')
    


# trecho da app
app.run(host='0.0.0.0', port=8080, debug=True)