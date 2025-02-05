from sqlalchemy import Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from datetime import datetime
from database import db

class Bebe(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    mae_id: Mapped[int] = mapped_column(ForeignKey('mae.id'))
    medico_id: Mapped[int] = mapped_column(ForeignKey('medico.id'))
    nome: Mapped[str]
    data_nascimento: Mapped[datetime] 
    peso: Mapped[float]
    altura: Mapped[float]

    

    def __init__(self, mae_id, medico_id, nome, data_nascimento, peso, altura):
        self.nome = nome
        self.mae_id = mae_id
        self.medico_id = medico_id
        self.data_nascimento = data_nascimento
        self.peso = peso
        self.altura = altura

    mae = relationship('Mae', backref='bebes')  # Relacionamento com Mae
    medico = relationship('Medico', backref='bebes')  # Relacionamento com Medico

class Mae(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    telefone: Mapped[str] = mapped_column(unique=True)
    idade: Mapped[int]


    def __init__(self, nome, telefone, idade):
        self.nome = nome
        self.telefone = telefone
        self.idade = idade


class Medico(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    CRM: Mapped[int] = mapped_column(unique=True)
    nome: Mapped[str]
    telefone: Mapped[str] = mapped_column(unique=True)

    def __init__(self, CRM, nome, telefone):
        self.CRM = CRM
        self.nome = nome
        self.telefone = telefone