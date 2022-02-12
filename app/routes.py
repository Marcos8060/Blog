from crypt import methods
from app import app
from app.forms import RegisterForm
from app.models import User
from crypt import methods
from flask import render_template,request, redirect,url_for,flash,abort
from flask_login import login_user,logout_user,login_required,current_user
from app import app
from app.models import User,Blog
from app import db
from app.forms import RegisterForm,LoginForm
from flask_login import login_required, login_user
from flask_mail import Mail,Message


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'marcosgav80@gmail.com'
app.config['MAIL_PASSWORD'] = 'gxgoeioxyktvhzab'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/signUp',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data,password=form.password1.data)
        message = Message('BlogHub',sender='marcosgav80@gmail.com',recipients=([form.email.data]))
        message.body = f'Thank you {form.username.data} and welcome to Pitch Lab Community where we turn your dreams into reality'
        mail.send(message)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome to BlogHub to proceed, kindly login',category='success')
        return redirect('blogs')
    if form.errors != {}:
        for error_message in form.errors.values():
            flash(f'There was an error with creating a user: {error_message}',category='danger')
    return render_template('signUp.html',form=form) 

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}',category='success')
            return redirect(url_for('blogs'))
        else:
            flash('Username and password do not match! Please try again',category='danger')
    return render_template('login.html',form=form)

@app.route('/blogs',methods=['GET','POST'])
@login_required
def blogs():
    blog = Blog
    if request.method == 'POST':
        title = request.form['title']
        blog = request.form['blog']
        print(title,blog)
        new_blog = Blog(title,blog,user_id=current_user.id)
        db.session.add(new_blog)
        db.session.commit()
    blogs = Blog.query.all()
    return render_template('blog.html',blogs=blogs)
