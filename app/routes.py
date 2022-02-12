from crypt import methods
from app import app
from app.forms import RegisterForm
from app.models import User
from crypt import methods
from flask import render_template,request, redirect,url_for,flash,abort
from flask_login import login_user,logout_user,login_required,current_user
from app import app
from app.models import User
from app import db
from app.forms import RegisterForm
from flask_login import login_required, login_user
from flask_mail import Mail,Message


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'marcosgav80@gmail.com'
app.config['MAIL_PASSWORD'] = 'gxgoeioxyktvhzab'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signUp',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data,password=form.password1.data)
        message = Message('Pitch Lab',sender='marcosgav80@gmail.com',recipients=([form.email.data]))
        message.body = f'Thank you {form.username.data} and welcome to Pitch Lab Community where we turn your dreams into reality'
        mail.send(message)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome to Pitchlab to proceed, kindly login',category='success')
    if form.errors != {}:
        for error_message in form.errors.values():
            flash(f'There was an error with creating a user: {error_message}',category='danger')
    return render_template('signUp.html',form=form) 

@app.route('/login')
def login():
    return render_template('login.html')
