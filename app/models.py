from sqlalchemy import ForeignKey
from app import db,login_manager
from app import bcrypt
from flask_login import UserMixin
import sys
from werkzeug.security import generate_password_hash,check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# user table
class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30),nullable=False, unique=True)
    email = db.Column(db.String(length=50),nullable=False,unique=True)
    password_hash = db.Column(db.String(255),nullable=False)
    blog = db.relationship('Blog',backref='owned_user',lazy='dynamic')



    sys.setrecursionlimit(1500)
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
 

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200))
    blogs = db.Column(db.String(5000))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comment_id = db.Column(db.Integer,db.ForeignKey('comments.id'))

    def __init__(self,title,blogs,user_id):
        self.title = title
        self.blogs = blogs
        self.user_id = user_id

class Comment(db.Model):
    __tablename__='comments'

    id = db.Column(db.Integer,primary_key=True)
    comments = db.Column(db.String(1400))
    blogs = db.relationship('Blog',backref='comment',lazy='dynamic')

    def __init__(self,comments):
        self.comments = comments
