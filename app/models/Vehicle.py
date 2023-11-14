from app import db

class Vehicle(db.Model):

    __tablename__ = 'vehicle'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    license_plate = db.Column(db.String(5))
    type_vehicle = db.Column(db.String(10))
    color = db.Column(db.String(50))
    number_seats = db.Column(db.Integer)
    additional_features = db.Column(db.String(50))
    notes = db.Column(db.String(10))

    carpool_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    carpool = db.relationship('Carpool', back_populates='vehicle')

