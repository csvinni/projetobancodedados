from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_mysqldb import MySQL
from database import mysql  # Certifique-se de ter inicializado o MySQL aqui
from datetime import datetime


campanha_bp = Blueprint('campanha', __name__, template_folder='templates')

@campanha_bp.route('/campanhas', methods=['GET', 'POST'])
@login_required
def campanhas():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        meta_financeira = request.form.get('meta_financeira')
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')
        status = request.form.get('status')

        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO campanhas (titulo, descricao, meta_financeira, data_inicio, data_fim, status, admin_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                       (titulo, descricao, meta_financeira, data_inicio, data_fim, status, current_user.id))
        mysql.connection.commit()
        cursor.close()
        
        flash('Campanha criada com sucesso!')
        return redirect(url_for('campanha.listar_campanhas'))

    return render_template('campanha/cadastro_campanhas.html')

@campanha_bp.route('/listar_campanhas', methods=['GET'])
@login_required
def listar_campanhas():
    data_inicial = request.args.get('data-inicial')
    data_final = request.args.get('data-final')

    cursor = mysql.connection.cursor()
    
    if current_user.is_admin():
        # Administrador: retorna todas as campanhas
        cursor.execute("SELECT * FROM campanhas")
    else:
        # Doador: retorna campanhas associadas ao doador
        cursor.execute("SELECT * FROM campanhas WHERE admin_id = %s", (current_user.id,))

    campanhas = cursor.fetchall()

    if data_inicial and data_final:
        campanhas = [campanha for campanha in campanhas if campanha[4] >= data_inicial and campanha[5] <= data_final]  # Ajuste os índices conforme necessário
    elif data_inicial:
        campanhas = [campanha for campanha in campanhas if campanha[4] >= data_inicial]
    elif data_final:
        campanhas = [campanha for campanha in campanhas if campanha[5] <= data_final]

    cursor.close()

    # Renderiza o template baseado no tipo de usuário
    if current_user.is_admin():
        return render_template('campanha/listar_campanhas.html', campanhas=campanhas)
    else:
        return render_template('campanha/listar_campanhas_doador.html', campanhas=campanhas)

@campanha_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM campanhas WHERE id = %s", (id,))
    campanha = cursor.fetchone()
    cursor.close()

    if not campanha:
        flash('Campanha não encontrada.')
        return redirect(url_for('campanha.listar_campanhas'))

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        meta_financeira = request.form.get('meta_financeira')
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')
        status = request.form.get('status')

        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE campanhas SET titulo = %s, descricao = %s, meta_financeira = %s, data_inicio = %s, data_fim = %s, status = %s WHERE id = %s", 
                       (titulo, descricao, meta_financeira, data_inicio, data_fim, status, id))
        mysql.connection.commit()
        cursor.close()
        
        flash('Campanha atualizada com sucesso!')
        return redirect(url_for('campanha.listar_campanhas'))

    return render_template('campanha/editar_campanha.html', campanha=campanha)

@campanha_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    cursor = mysql.connection.cursor()
    
    # Excluir doações associadas
    cursor.execute("DELETE FROM doacoes WHERE id_campanha = %s", (id,))
    
    # Excluir a campanha
    cursor.execute("DELETE FROM campanhas WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()

    flash('Campanha e doações associadas excluídas com sucesso!', 'success')
    return redirect(url_for('campanha.listar_campanhas'))