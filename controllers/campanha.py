from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.models import Doacao, Campanha
from database.config import Session 
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

campanha_bp = Blueprint('campanha', __name__, template_folder='templates')
session = Session()

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

        nova_campanha = Campanha(
            titulo=titulo,
            descricao=descricao,
            meta_financeira=meta_financeira,
            data_inicio=data_inicio,
            data_fim=data_fim,
            status=status,
            admin_id=current_user.id
        )

        session.add(nova_campanha)
        session.commit()
        flash('Campanha criada com sucesso!')
        return redirect(url_for('campanha.listar_campanhas'))

    return render_template('campanha/cadastro_campanhas.html')

@campanha_bp.route('/listar_campanhas', methods=['GET'])
@login_required
def listar_campanhas():
    data_inicial = request.args.get('data-inicial')
    data_final = request.args.get('data-final')

    query = session.query(Campanha).filter_by(admin_id=current_user.id)

    if data_inicial and data_final:
        query = query.filter(and_(Campanha.data_inicio >= data_inicial, Campanha.data_fim <= data_final))
    elif data_inicial:
        query = query.filter(Campanha.data_inicio >= data_inicial)
    elif data_final:
        query = query.filter(Campanha.data_fim <= data_final)
    campanhas = query.all()

    return render_template('campanha/listar_campanhas.html', campanhas=campanhas)

@campanha_bp.route('/concluida/<int:id>', methods=['POST'])
@login_required
def concluida(id):
    campanha = session.get(Campanha, id)
    if campanha:
        campanha.status = 'Concluída'
        session.commit()
        flash('Campanha concluída com sucesso!')
    else:
        flash('Campanha não encontrada.')
    
    return redirect(url_for('campanha.listar_campanhas'))

@campanha_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    campanha = session.get(Campanha, id)
    if not campanha:
        flash('Campanha não encontrada.')
        return redirect(url_for('campanha.listar_campanhas'))

    if request.method == 'POST':
        campanha.titulo = request.form.get('titulo')
        campanha.descricao = request.form.get('descricao')
        campanha.meta_financeira = request.form.get('meta_financeira')
        campanha.data_inicio = datetime.strptime(request.form.get('data_inicio'), '%Y-%m-%d').date()
        campanha.data_fim = datetime.strptime(request.form.get('data_fim'), '%Y-%m-%d').date()
        campanha.status = request.form.get('status')

        
        session.commit()
        flash('Campanha atualizada com sucesso!')
        return redirect(url_for('campanha.listar_campanhas'))

    return render_template('campanha/editar_campanha.html', campanha=campanha)
