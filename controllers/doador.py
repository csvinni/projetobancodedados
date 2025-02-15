from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from database.config import Session
from models.models import Doador
from flask_login import login_required, current_user

doador_bp = Blueprint('doador', __name__, template_folder='templates')
session = Session()

@doador_bp.route('/cadastrodoador', methods=['GET', 'POST'])
def cadastrodoador():
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')

        novo_doador = Doador(nome=nome, email=email, telefone=telefone, admin_id=current_user.id)

        try:
            session.add(novo_doador)
            session.commit()
            flash('Doador cadastrado com sucesso!')
            return redirect(url_for('doacao.itens_doacao'))
        except SQLAlchemyError:
            session.rollback()
            flash('Erro ao cadastrar doador. Tente novamente mais tarde.')
    session.close()
    return render_template('doador/cadastro_doador.html')

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

@doador_bp.route('/doador/edit/<int:doador_id>', methods=['GET', 'POST'])
def editar_doador(doador_id):
    session = Session()
    doador = session.query(Doador).get(doador_id)

    if request.method == 'POST':
        doador.nome = request.form.get('nome')
        doador.telefone = request.form.get('telefone')
        doador.email = request.form.get('email')

        try:
            session.commit()
            flash('Doador atualizado com sucesso!')
            return redirect(url_for('doacao.itens_doacoes'))
        except SQLAlchemyError:
            session.rollback()
            flash('Erro ao atualizar doador. Tente novamente mais tarde.')

    session.close()
    return render_template('doador/cadastro_doador.html', doador=doador)

@doador_bp.route('/doador/<int:doador_id>', methods=['GET'])
def detalhes_doador(doador_id):
    session = Session()
    doador = session.query(Doador).get(doador_id)
    session.close()

    if doador is None:
        flash('Doador não encontrado.')
        return redirect(url_for('doador.doador'))

    return render_template('doador/cadastro_doador.html', doador=doador)
