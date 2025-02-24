from flask_login import UserMixin
from datetime import date
from database.config import Base
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import mapped_column, Mapped, relationship
from  sqlalchemy import Text, Integer, ForeignKey, Date, Float
# importei isso 
from typing import List

class Admin(UserMixin, Base):
    __tablename__ = 'admin'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(Text, nullable=False)
    ong: Mapped[str] = mapped_column(Text, nullable=False)
#modifiquei essa duas linhas 
    from typing import List

    campanhas: Mapped[List['Campanha']] = relationship('Campanha', back_populates='admin')
    def is_admin(self):
        return True 

    def set_password(self, password: str):
        self.senha = generate_password_hash(password) 
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.senha, password) 
    def get_id(self):
        return str(self.id)
    

class Doador(UserMixin,Base):
    __tablename__ = 'doadores'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    senha: Mapped[str] = mapped_column(Text, nullable=False)
    telefone: Mapped[str] = mapped_column(Text, nullable=False)


    #doacoes: Mapped[list['Doacao']] = relationship('Doacao', back_populates='doador')
    
    doacoes: Mapped[List['Doacao']] = relationship('Doacao', back_populates='doador')
    def is_admin(self):
        return False

    def set_password(self, password: str):
        self.senha = generate_password_hash(password) 
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.senha, password) 
    def get_id(self):
        return str(self.id)
    


class Campanha(Base):
    __tablename__ = 'campanhas'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(Text, nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    meta_financeira: Mapped[str] = mapped_column(Text, nullable=False)
    data_inicio: Mapped[Date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    data_fim: Mapped[Date] = mapped_column(Date)

    admin_id: Mapped[int] = mapped_column(Integer, ForeignKey('admin.id'))
    admin: Mapped['Admin'] = relationship('Admin', back_populates='campanhas')
    #doacoes: Mapped[list['Doacao']] = relationship('Doacao', back_populates='campanha')
    doacoes: Mapped[List['Doacao']] = relationship('Doacao', back_populates='campanha')
    

class Doacao(Base):
    __tablename__ = 'doacoes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_doador: Mapped[int] = mapped_column(Integer, ForeignKey('doadores.id'), nullable=False)
    id_campanha: Mapped[int] = mapped_column(Integer, ForeignKey('campanhas.id'), nullable=False)
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    data_doacao: Mapped[date] = mapped_column(Date, nullable=False)

    doador = relationship('Doador', back_populates='doacoes')
    campanha = relationship('Campanha', back_populates='doacoes')


class Relatorio(Base):
    __tablename__ = 'relatorios'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_campanha: Mapped[int] = mapped_column(Integer, ForeignKey('campanhas.id'))
    data_referencia: Mapped[Date] = mapped_column(Date)
    total: Mapped[float] = mapped_column(Float)
    total_itens_doados: Mapped[int] = mapped_column(Integer, nullable=False)
    meta_comparativo: Mapped[str] = mapped_column(Text, nullable=False)

    campanha: Mapped['Campanha'] = relationship('Campanha')
