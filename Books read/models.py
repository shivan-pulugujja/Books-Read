from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'Users'
    uname = db.Column(db.String,primary_key=True)
    firstname = db.Column(db.String,nullable=False)
    lastname = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False)
    pwd = db.Column(db.String,nullable=False)
    # recorded_time = db.Column(db.DateTime, server_default=db.func.now())


class Bookdetails(db.Model):
    __tablename__= 'Bookdetails'
    id = db.Column(db.String,primary_key=True)
    title = db.Column(db.String,nullable=False)
    author = db.Column(db.String,nullable=False)
    year = db.Column(db.String,nullable=False)
    


