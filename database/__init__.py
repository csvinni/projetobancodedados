from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv

from .config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB

mysql = MySQL()

app = Flask(__name__)
load_dotenv('.env')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'  # Alterado para 'root'
app.config['MYSQL_PASSWORD'] = '1234'  # Alterado para a nova senha
app.config['MYSQL_DB'] = 'db_banco'  # Substitua pelo seu banco de dados
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

conexao = MySQL(app)

def banco(banco_dados):
    with app.app_context():
        cursor = conexao.connection.cursor()
        with open(banco_dados, 'r') as file:
            sql = file.read()
            comandos_raw = sql.split(';') 

            commands = [comando.strip() for comando in comandos_raw if comando.strip()]

            for command in commands: 
                cursor.execute(command) 
        conexao.connection.commit()
        cursor.close()

if __name__ == "__main__":
    banco('mysql.sql') 
    print("Banco de dados e tabelas inicializados com sucesso!")