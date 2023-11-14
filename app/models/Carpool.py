from app import db
from .User import User

class Carpool(User):

    __tablename__ = 'carpool'

    id_carpool = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
         
    __mapper__args__ = {
        'polymorphic_identity':'carpool',
    }

    zone = db.Column(db.String(140))
    vehicle = db.relationship('Vehicle', back_populates='carpool', uselist=False)
