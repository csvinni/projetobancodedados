from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from database.config import Session
from models.models import Doador, Doacao, Campanha
from datetime import datetime
from flask_login import login_required, current_user
from sqlalchemy import and_

doador_bp = Blueprint('doador', __name__, template_folder='templates')
session = Session()

@doador_bp.route('/indexdoador')
@login_required
def indexdoador():
    return render_template('doador/indexdoador.html')


@doador_bp.route('/cadastrodoador', methods=['GET', 'POST'])
def cadastrodoador():
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        senha = request.form.get('senha')

        novo_doador = Doador(nome=nome, email=email, telefone=telefone)
        novo_doador.set_password(senha) 

        try:
            session.add(novo_doador)
            session.commit()
            flash('Doador cadastrado com sucesso!')
            return redirect(url_for('auth.login'))
        except SQLAlchemyError:
            session.rollback()
            flash('Erro ao cadastrar doador. Tente novamente mais tarde.')
    session.close()
    return render_template('doador/cadastro_doador.html')


@doador_bp.route('/itens_doacao', methods=['GET', 'POST'])
@login_required
def itens_doacao():
    session = Session()

    if request.method == 'POST':
        print("Dados recebidos:", request.form) 

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
        session.add(nova_doacao)
        session.close()  

    campanhas = session.query(Campanha).all()
    session.close()  
    return render_template('doador/itens_doacoes.html', campanhas=campanhas)


@doador_bp.route('/listar', methods=['GET'])
@login_required
def listar():
    try:
        doadores = session.query(Doador).filter_by(admin_id=current_user.id).all()
        return render_template('doador/listar_doadores.html', doadores=doadores)
    except SQLAlchemyError:
        flash('Erro ao buscar doadores. Tente novamente mais tarde.')
        return redirect(url_for('doacao.itens_doacao'))
    finally:
        session.close()