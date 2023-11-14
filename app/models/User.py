from flask_login import UserMixin
from app import db
from .Comment import Comment
from flask import request, session, send_from_directory
from sqlalchemy import Date
from datetime import datetime


class User(UserMixin, db.Model):

    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    birth = db.Column(db.String(8), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(50), nullable=False, unique=True)
    whatsapp = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    avatar = db.Column(db.String(140))
    tipo = db.Column(db.String(40))
    type = db.Column(db.String(50)) # atributo discriminador

    __mapper__args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':type
    }

    # Retorna o id do usuário 
    def get_user_id(self):
        return id

    # Registrar usuário
    def registerUser(self):
        db.session.add(self)
        db.session.commit()

    # Verificar e-mail
    def verifyEmail(email):
        email_db = User.query.filter_by(email=email).first()
        return email_db
    
    # Deleta usuário
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    # Seleciona os comentários do usuário
    def get_comments(self):
        return Comment.query.filter(Comment.user_gotcomment_id == self.id).all()

    def get_age(self, data):
        data_nascimento = datetime.strptime(data, "%d/%m/%Y")
        data_atual = datetime.now()
        diferenca = data_atual - data_nascimento
        age = diferenca.days // 365

        return age