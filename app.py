from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL
from controllers.campanha import campanha_bp
from controllers.doacao import doacao_bp
from controllers.doador import doador_bp
from controllers.user import user_bp
from auth.bp import auth_bp, login_manager

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_banco'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

conexao = MySQL(app)

app.register_blueprint(auth_bp)
app.register_blueprint(doacao_bp)
app.register_blueprint(doador_bp)
app.register_blueprint(campanha_bp)
app.register_blueprint(user_bp)


@app.route('/')
def index():
    return render_template('index.html')
