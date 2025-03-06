from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import obter_admin, obter_doador, Admin, Doador  # Importando as classes
from models.models import mysql
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint('auth', __name__, template_folder='templates')

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM admin WHERE id = %s", (user_id,))
    admin_data = cursor.fetchone()
    if admin_data:
        return Admin(admin_data['id'], admin_data['nome'], admin_data['email'], admin_data['senha'], admin_data['ong'])

    cursor.execute("SELECT * FROM doadores WHERE id = %s", (user_id,))
    doador_data = cursor.fetchone()
    if doador_data:
        return Doador(doador_data['id'], doador_data['nome'], doador_data['email'], doador_data['telefone'], doador_data['senha'])

    cursor.close()
    return None

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

        if role == 'Admin':
            admin = obter_admin(email)
            if admin and check_password_hash(admin.senha, senha):
                login_user(admin)
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('auth.indexadmin'))

        elif role == 'doador':
            doador = obter_doador(email)
            if doador and check_password_hash(doador.senha, senha):
                login_user(doador)
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('doador.indexdoador'))

        flash('Email ou senha incorretos', 'error')

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



