from website import db
from flask_login import UserMixin

class Notes(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    note = db.Column(db.String(250))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

class Users(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)   
    name = db.Column(db.String(25))
    email = db.Column(db.String(35),unique = True)
    password = db.Column(db.String(25))
    notes = db.relationship('Notes')
