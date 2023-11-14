from app import db
from app.models.User import User
from app.models.Student import Student
from app.models.Carpool import Carpool

class Search(db.Model):

    __tablename__ = 'search'
    
    id = db.Column(db.Integer, primary_key=True)
    searchInput = db.Column(db.String(50))
    
    def searchName(self, searchInput, typeUser:any):
        users = typeUser.query
        users = users.filter(typeUser.username.like('%' + searchInput + '%'))
        users = users.order_by(typeUser.username).all()
        return users
