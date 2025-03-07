from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_mysqldb import MySQL
from datetime import datetime
from database import mysql  

doacao_bp = Blueprint('doacao', __name__, template_folder='templates')

@doacao_bp.route('/itens_doacao', methods=['GET', 'POST'])
@login_required
def itens_doacao():
    if request.method == 'POST':
        print("Dados recebidos:", request.form)  # Para depuração

        id_campanha = request.form.get('id_campanha')
        tipo_doacao = request.form.get('tipo_doacao')
        data_doacao = request.form.get('data_doacao')
        data_doacao = datetime.strptime(data_doacao, '%Y-%m-%d').date()

        tipo_item = request.form.get('tipo_item') if tipo_doacao == "Item" else None
        quantidade = request.form.get('quantidade') if tipo_doacao == "Item" else None
        valor = request.form.get('valor') if tipo_doacao == "Dinheiro" else None

        cursor = mysql.connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO doacoes (id_doador, id_campanha, tipo_doacao, tipo_item, quantidade, valor, data_doacao) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (current_user.id, int(id_campanha), tipo_doacao, tipo_item, quantidade, valor, data_doacao))
            
            mysql.connection.commit()

        except Exception as e:
            mysql.connection.rollback()
            print(f"Erro ao registrar a doação: {e}")  # Para depuração

        finally:
            cursor.close()  
            return redirect(url_for('campanha.listar_campanhas_doador'))

    # Buscar campanhas disponíveis para exibição no formulário
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM campanhas")  
    campanhas = cursor.fetchall()
    cursor.close()  

    return render_template('doacao/cadastro_itens_doacao.html', campanhas=campanhas)


@doacao_bp.route('/listar_doacoes', methods=['GET'])
@login_required
def listar_doacoes():

    print(f"Usuário autenticado: {current_user.is_authenticated}")
    print(f"Usuário: {current_user}")
    print(f"Usuário é admin? {current_user.is_admin()}")

    if not current_user.is_admin():  
        return render_template('403.html')
    
    cursor = mysql.connection.cursor()
    
    cursor.execute("""
        SELECT 
            doacoes.tipo_doacao, 
            doacoes.tipo_item, 
            doacoes.quantidade, 
            doacoes.valor, 
            doacoes.data_doacao, 
            doadores.nome AS doador_nome, 
            campanhas.titulo AS campanha_titulo 
        FROM doacoes 
        JOIN doadores ON doacoes.id_doador = doadores.id 
        JOIN campanhas ON doacoes.id_campanha = campanhas.id 
    """)
    
    doacoes = cursor.fetchall()
    cursor.close() 
    
    return render_template('doacao/listar_doacoes.html', doacoes=doacoes)


@doacao_bp.route('/total_doado', methods=['GET', 'POST'])
@login_required
def total_doado():
    # Verifica se o usuário é admin
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', lambda: False)():
        return render_template('403.html')

    total = 0  # Inicializa como 0 para evitar erros de NoneType
    doacoes = []
    doadores = []  # Lista para armazenar os doadores

    cursor = mysql.connection.cursor()
    try:
        # Buscar todos os doadores cadastrados
        cursor.execute("SELECT id, nome FROM doadores")
        doadores = cursor.fetchall()  # Retorna uma lista de tuplas [(id, nome), ...]

    except Exception as e:
        flash(f'Erro ao carregar doadores: {e}', 'error')
    
    if request.method == 'POST':
        p_id_doador = request.form.get('id_doador')
        p_data_inicio = request.form.get('data_inicio')
        p_data_fim = request.form.get('data_fim')

        if not (p_id_doador and p_data_inicio and p_data_fim):
            flash('Todos os campos são obrigatórios!', 'warning')
        else:
            try:
                # Chamada do procedimento armazenado para calcular o total doado
                cursor.execute("SELECT total_doado(%s, %s, %s)", (p_id_doador, p_data_inicio, p_data_fim))
                resultado = cursor.fetchone()
                total = resultado[0] if resultado and resultado[0] is not None else 0  # Evita erro de NoneType
                
                # Busca as doações correspondentes
                cursor.execute("""
                    SELECT 
                        doacoes.tipo_doacao, 
                        doacoes.tipo_item, 
                        doacoes.quantidade, 
                        doacoes.valor, 
                        doacoes.data_doacao, 
                        doadores.nome AS doador_nome, 
                        campanhas.titulo AS campanha_titulo 
                    FROM doacoes 
                    JOIN doadores ON doacoes.id_doador = doadores.id 
                    JOIN campanhas ON doacoes.id_campanha = campanhas.id 
                    WHERE doacoes.id_doador = %s AND doacoes.data_doacao BETWEEN %s AND %s
                """, (p_id_doador, p_data_inicio, p_data_fim))
                doacoes = cursor.fetchall()

            except Exception as e:
                flash(f'Erro ao calcular total doado: {e}', 'error')
    
    cursor.close()

    return render_template('doacao/listar_doacoes.html', total=total, doacoes=doacoes, doadores=doadores)

