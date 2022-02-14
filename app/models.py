from email.policy import default
from time import timezone
from sqlalchemy import ForeignKey, func
from app import db,login_manager
from app import bcrypt,app
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
    comments = db.relationship('Comment',backref='owned_user',lazy='dynamic')





    sys.setrecursionlimit(1500)
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
 

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200))
    blogs = db.Column(db.String(5000))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comments = db.relationship('Comment',backref='blog')

    def __init__(self,title,blogs):
        self.title = title
        self.blogs = blogs


class Comment(db.Model):
    __tablename__='comments'

    id = db.Column(db.Integer,primary_key=True)
    comments = db.Column(db.String(255))
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))
    author = db.Column(db.Integer,db.ForeignKey('users.id'))

    def __init__(self,comments,author,blog_id):
        self.comments = comments
        self.author = author
        self.blog_id = blog_id

@app.before_first_request
def create_tables():
    db.create_all()

