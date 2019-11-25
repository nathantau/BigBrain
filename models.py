import bcrypt
from app import app, db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    salt = db.Column(db.String(255), primary_key=True, nullable=False)
    email = db.Column(db.String(255), primary_key=True, nullable=False)
    password = db.Column(db.String(255), primary_key=True, nullable=False)
    
    def __init__(self, email, password):
        self.email = email
        self.salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password=password, salt=self.salt)

    def save(self):
        db.session.add(self)
        db.session.commit()