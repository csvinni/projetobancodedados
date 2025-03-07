from flask_mysqldb import MySQL
from flask_login import UserMixin


mysql = MySQL()

class Admin(UserMixin):
    def __init__(self, id, nome, email, senha, ong):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ong = ong
        

    def get_id(self):
        return self.id

    def is_admin(self):
        return True  # Sempre retorna True para admins


class Doador(UserMixin):
    def __init__(self, id, nome, email, telefone, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.senha = senha

    def get_id(self):
        return self.id

    def is_admin(self):
        return False  # Doador não é admin

def obter_admin(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM admin WHERE email = %s", (email,))
    admin_data = cursor.fetchone()
    cursor.close()

    if admin_data:
        return Admin(admin_data['id'], admin_data['nome'], admin_data['email'], admin_data['senha'], admin_data['ong'])
    return None

def obter_doador(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM doadores WHERE email = %s", (email,))
    doador_data = cursor.fetchone()
    cursor.close()

    if doador_data:
        return Doador(doador_data['id'], doador_data['nome'], doador_data['email'], doador_data['telefone'], doador_data['senha'])
    return None