from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, template_folder='templates')
mysql = MySQL()  # Inicialize o MySQL aqui
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM admin WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if user is None:
        cursor.execute("SELECT * FROM doadores WHERE id = %s", (user_id,))
        user = cursor.fetchone()
    cursor.close()
    return user

@auth_bp.route('/indexadmin')
@login_required
def indexadmin():
    return render_template('auth/indexadmin.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        role = request.form.get('role')

        cursor = mysql.connection.cursor()
        
        if role == 'Admin':
            cursor.execute("SELECT * FROM admin WHERE email = %s", (email,))
            admin = cursor.fetchone()
            if admin and check_password_hash(admin[3], senha):  # Assuming senha is at index 3
                login_user(admin)
                return redirect(url_for('auth.indexadmin'))

        elif role == 'doador':
            cursor.execute("SELECT * FROM doadores WHERE email = %s", (email,))
            doador = cursor.fetchone()
            if doador and check_password_hash(doador[3], senha):  # Assuming senha is at index 3
                login_user(doador)
                return redirect(url_for('doador.indexdoador'))

        cursor.close()

    return render_template('auth/login.html')

@auth_bp.route('/cadastro_admin', methods=['GET', 'POST'])
def cadastro_admin():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        ong = request.form['ong']
        senha = request.form['senha']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO admin (nome, email, ong, senha) VALUES (%s, %s, %s, %s)", 
                       (nome, email, ong, generate_password_hash(senha)))
        mysql.connection.commit()
        cursor.close()

        flash('Administrador cadastrado com sucesso!')
        return redirect(url_for('auth.login'))

    return render_template('auth/cadastro_admin.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('auth/indexadmin.html', nome=current_user.ong)