from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_mysqldb import MySQL
from datetime import datetime
from database import mysql  # Certifique-se de ter inicializado o MySQL aqui

doacao_bp = Blueprint('doacao', __name__, template_folder='templates')

@doacao_bp.route('/itens_doacao', methods=['GET', 'POST'])
@login_required
def itens_doacao():
    if request.method == 'POST':
        print("Dados recebidos:", request.form)  # Para depuração

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
            return redirect(url_for('doacao.itens_doacao'))
        finally:
            cursor.close()  

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM campanhas")  # Ajuste conforme o nome real da tabela
    campanhas = cursor.fetchall()
    cursor.close()  
    return render_template('doacao/cadastro_itens_doacao.html', campanhas=campanhas)

@doacao_bp.route('/listar_doacoes', methods=['GET'])
@login_required
def listar_doacoes():
    cursor = mysql.connection.cursor()
    
    cursor.execute("""
        SELECT 
            doacoes.valor, 
            doacoes.data_doacao, 
            doadores.nome AS doador_nome, 
            campanhas.titulo AS campanha_titulo 
        FROM doacoes 
        JOIN doadores ON doacoes.id_doador = doadores.id 
        JOIN campanhas ON doacoes.id_campanha = campanhas.id 
        WHERE campanhas.admin_id = %s
    """, (current_user.id,))
    
    doacoes = cursor.fetchall()
    cursor.close() 
    
    return render_template('doacao/listar_doacoes.html', doacoes=doacoes)