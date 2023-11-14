from app import db

class Address(db.Model):

    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(db.String(10))
    street = db.Column(db.String(100))
    number = db.Column(db.String(5))
    neighborhood = db.Column(db.String(10))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))

    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    student = db.relationship('Student', back_populates='address')
