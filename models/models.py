from flask_mysqldb import MySQL

mysql = MySQL(app)

def adicionar_admin(nome, email, senha, ong):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO admin (nome, email, senha, ong) VALUES (%s, %s, %s, %s)", (nome, email, senha, ong))
    mysql.connection.commit()
    cursor.close()

def obter_admin(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM admin WHERE email = %s", (email,))
    admin = cursor.fetchone()
    cursor.close()
    return admin