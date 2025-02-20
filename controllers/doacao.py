from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.models import Doacao, Doador, Campanha
from database.config import Session 
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

doacao_bp = Blueprint('doacao', __name__, template_folder='templates')
session = Session()

@doacao_bp.route('/itens_doacao', methods=['GET', 'POST'])
@login_required
def itens_doacao():
    session = Session()

    if request.method == 'POST':
        print("Dados recebidos:", request.form)  # Para depuração

        id_campanha = request.form.get('id_campanha')
        valor = request.form.get('valor')
        data_doacao = request.form.get('data_doacao')
        data_doacao = datetime.strptime(data_doacao, '%Y-%m-%d').date()

        nova_doacao = Doacao(
            id_doador=current_user.id,
            id_campanha=int(id_campanha),
            valor=float(valor),
            data_doacao=data_doacao
        )

        try:
            session.add(nova_doacao)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao registrar a doação: {e}")  # Para depuração
            flash('Erro ao registrar a doação. Tente novamente mais tarde.')
            return redirect(url_for('doacao.itens_doacao'))
        finally:
            session.close()  

    campanhas = session.query(Campanha).all()
    session.close()  
    return render_template('doacao/cadastro_itens_doacao.html', campanhas=campanhas)

@doacao_bp.route('/listar_doacoes', methods=['GET'])
@login_required
def listar_doacoes():
    doacoes = (
        session.query(
            Doacao.valor,  # Pegando o valor da doação
            Doacao.data_doacao,  # Pegando a data da doação
            Doador.nome.label('doador_nome'),
            Campanha.titulo.label('campanha_titulo')
        )
        .join(Doador, Doacao.id_doador == Doador.id)
        .join(Campanha, Doacao.id_campanha == Campanha.id)
        .filter(Campanha.admin_id == current_user.id)  # Filtra por admin logado
        .all())

    session.close() 
    return render_template('doacao/listar_doacoes.html', doacoes=doacoes)