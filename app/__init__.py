from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from  flask_migrate import Migrate, MigrateCommand
import os

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://marcos:getaways@localhost/blog_hub'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')




app.config['SECRET_KEY'] = '944d51c0258f07f940b031b2'
login_manager = LoginManager(app)

db = SQLAlchemy(app)
@app.before_first_request
def create_tables():
    db.create_all()
migrate = Migrate(app,db)
bcrypt = Bcrypt(app)
from app import routes