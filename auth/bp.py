from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from models.models import Admin
from database.config import Session 

auth_bp = Blueprint('auth', __name__, template_folder='templates')
session = Session()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return session.query(Admin).get(int(user_id))  

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        admin = session.query(Admin).filter_by(email=email).first()
        if admin and admin.senha == senha: 
            login_user(admin)
            return redirect(url_for('auth.dashboard'))
        flash('Credenciais inválidas.')
    return render_template('auth/login.html')

@auth_bp.route('/cadastro_admin', methods=['GET', 'POST'])
def cadastro_admin():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        ong = request.form['ong']
        senha = request.form['senha']

        novo_admin = Admin(nome=nome,email=email,senha=senha,ong=ong)
        session.add(novo_admin)
        session.commit()

        flash('Administrador cadastrado com sucesso!')
        return redirect(url_for('auth.login'))

    return render_template('auth/cadastro_admin.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('auth/indexadmin.html', nome=current_user.nome)