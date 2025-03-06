from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv('.env')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_banco'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

def banco(banco_dados):
    with app.app_context():
        cursor = mysql.connection.cursor()
        with open(banco_dados, 'r') as file:
            sql = file.read()
            comandos_raw = sql.split(';')

            commands = []
            for comando in comandos_raw:
                comando_limpo = comando.strip()
                if comando_limpo:
                    commands.append(comando_limpo)

            for command in commands:
                print(f"Executando: {command}")  # Adicionando um print para ver qual comando está sendo executado
                cursor.execute(command)
        mysql.connection.commit()
        cursor.close()

if __name__ == "__main__":
    banco('mysql.sql')  
    print("Banco de dados e tabelas inicializados com sucesso!")