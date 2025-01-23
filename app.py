from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL
from dotenv import load_dotenv


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_banco'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

conexao = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/edicao')
def edicao():
    return render_template('edicao.html')

@app.route('/doador', methods = (['GET', 'POST']))
def doador():
    return render_template('doador.html')

@app.route('/campanhas',  methods = (['GET', 'POST']))
def campanhas():
    return  render_template('campanhas.html')

@app.route('/itens_doacoes',  methods = (['GET', 'POST']))
def itens_doacoes():
    return  render_template('itens_doacoes.hthml')

@app.route('/listar_campanhas',  methods = (['GET', 'POST']))
def listar_campanhas():
    return  render_template('listar_campanhas.hthml')


@app.route('/listar_doadores',  methods = (['GET', 'POST']))
def listar_doadores():
    return  render_template('listar_doadores.hthml')

@app.route('/relatorios',  methods = (['GET', 'POST']))
def relatorios():
    return  render_template('relatorios.hthml')

