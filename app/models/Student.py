from app import db
from .User import User

class Student(User):

    __tablename__ = 'student'

    id_student = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    
    __mapper__args__ = {
        'polymorphic_identity':'student',
    }

    school = db.Column(db.String(140))
    address = db.relationship('Address', back_populates='student', uselist=False)

