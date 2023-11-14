from app import db

class Comment(db.Model):

    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    user_docomment_id = db.Column(db.Integer, nullable=False)
    user_gotcomment_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment_text = db.Column(db.String(255), nullable=False)



    def doComment(self):
        db.session.add(self)
        db.session.commit()