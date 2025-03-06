from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv('.env')

# Configurações do Flask e MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '1234')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'db_banco')
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

def banco(banco_dados):
    with app.app_context():
        cursor = mysql.connection.cursor()
        with open(banco_dados, 'r') as file:
            sql = file.read()
            comandos_raw = sql.split(';') 
            commands = [comando.strip() for comando in comandos_raw if comando.strip()]

            for command in commands: 
                cursor.execute(command) 
        mysql.connection.commit()
        cursor.close()

if __name__ == "__main__":
    caminho_sql = os.path.join(os.path.dirname(__file__), 'mysql.sql')
    banco(caminho_sql) 
    print("Banco de dados e tabelas inicializados com sucesso!")

# Adicione esta linha para exportar mysql
__all__ = ['app', 'mysql']