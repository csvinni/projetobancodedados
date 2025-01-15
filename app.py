from flask import Flask , redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'pagina inicial'

@app.route('/edicao')
def edicao():
    return 'edicao'

@app.route('/cadastro_doador', methods = (['GET', 'POST']))
def cadastro_doador():
    return render_template('cadastro_doador.html')

@app.route('/cadastro_campanhas')
def cadastro_campanhas():
    return 'cadastro_campanhas'

@app.route('/cadastro_itens_doacoes')
def cadastro_itens_doacoes():
    return 'cadastro_itens_doacoes'

