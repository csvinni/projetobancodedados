from flask import Flask, render_template, url_for, request, redirect
from controllers.campanha import campanha_bp
from controllers.doacao import doacao_bp
from controllers.doador import doador_bp
from auth.bp import auth_bp, login_manager
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'dificil'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'  # Alterado para 'root'
app.config['MYSQL_PASSWORD'] = '1234'  # Alterado para a nova senha
app.config['MYSQL_DB'] = 'db_banco'  # Substitua pelo seu banco de dados
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
login_manager.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(doacao_bp)
app.register_blueprint(doador_bp)
app.register_blueprint(campanha_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)