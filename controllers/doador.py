from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user,  login_user
from database import mysql  # Certifique-se de ter inicializado o MySQL aqui

doador_bp = Blueprint('doador', __name__, template_folder='templates')


@doador_bp.route('/indexdoador')
@login_required
def indexdoador():
    return render_template('doador/indexdoador.html')

@doador_bp.route('/cadastrodoador', methods=['GET', 'POST'])
def cadastrodoador():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        senha = request.form['senha']
        hashed_senha = generate_password_hash(senha)

        cursor = mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO doadores (nome, email, telefone, senha) VALUES (%s, %s, %s, %s)",
                           (nome, email, telefone, hashed_senha))
            mysql.connection.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('auth.login'))  # Redireciona para a página de login
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao cadastrar: {e}', 'error')
        finally:
            cursor.close()
    
    return render_template('doador/cadastro_doador.html')

@doador_bp.route('/itens_doacao', methods=['GET', 'POST'])
@login_required
def itens_doacao():
    if request.method == 'POST':
        print("Dados recebidos:", request.form) 

        id_campanha = request.form.get('id_campanha')
        valor = request.form.get('valor')
        data_doacao = request.form.get('data_doacao')
        data_doacao = datetime.strptime(data_doacao, '%Y-%m-%d').date()

        cursor = mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO doacoes (id_doador, id_campanha, valor, data_doacao) VALUES (%s, %s, %s, %s)", 
                           (current_user.id, int(id_campanha), float(valor), data_doacao))
            mysql.connection.commit()
            flash('Doação registrada com sucesso!')
        except Exception as e:
            mysql.connection.rollback()
            print(f"Erro ao registrar a doação: {e}")  # Para depuração
            flash('Erro ao registrar a doação. Tente novamente mais tarde.')
        finally:
            cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM campanhas")  # Ajuste conforme o nome real da tabela
    campanhas = cursor.fetchall()
    cursor.close()  
    return render_template('doador/itens_doacoes.html', campanhas=campanhas)

@doador_bp.route('/listar', methods=['GET'])
@login_required
def listar():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT * FROM doadores WHERE admin_id = %s", (current_user.id,))
        doadores = cursor.fetchall()
        return render_template('doador/listar_doadores.html', doadores=doadores)
    except Exception as e:
        flash(f'Erro ao buscar doadores: {e}. Tente novamente mais tarde.')
        return redirect(url_for('doador.indexdoador'))
    finally:
        cursor.close()