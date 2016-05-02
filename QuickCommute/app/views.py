from flask import render_template, request, flash, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://websysS16GB6:websysS16GB6!!@websys3/websysS16GB6'
db = SQLAlchemy(app)

@app.route('/')
@app.route('/index')
def index():
  return render_template("commuterAppTemplate.html")

lm  = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

@lm.user_loader
def load_user(id):
  return User.query.get(int(id))

class User(db.Model):
  __tablename__ = "UserProfile"
  id = db.Column('UserId', db.Integer, primary_key=True)
  email = db.Column('email', db.String(45), index=True, unique=True)
  firstname = db.Column('FirstName', db.String(45))
  lastname = db.Column('LastName', db.String(45))
  password = db.Column('Password', db.String(128))
  registration_time = db.Column('RegistrationTime', db.DateTime)
    
  def __init__(self, email, firstname, lastname, password):
    self.email = email
    self.set_password(password)
    self.firstname = firstname
    self.lastname = lastname
    self.registered_time = datetime.utcnow()
 
  def set_password(self,password):
    self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password,password)

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    try:
      return unicode(self.id)  # python 2
    except NameError:
      return str(self.id)  # python 3
  
  def __repr__(self):
    return '<User %r>' % (self.firstname)

db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    return render_template('register.html')
  
  firstname = request.form['firstname']
  lastname = request.form['lastname']
  email = request.form['email']
  password = request.form['password']
  
  user = User(email,firstname,lastname,password)
  db.session.add(user)
  db.session.commit()

  flash('User registered successfully!!')
  return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')

  email = request.form['email']
  password = request.form['password']

  registered_user = User.query.filter_by(email=email).first()
  #registered_user = User.query.filter_by(email=email).first()
  flash(registered_user.check_password(registered_user.password))

  if registered_user.check_password(password):
    login_user(registered_user)
    flash('Logged in successfully')
    return ('{"%s":"success"}'%email)
  else:
    flash('Email or password is invalid', 'error')
    return ('{"%s":"failed"}' %email)

@app.route('/landing',methods=['GET','POST'])
def landing():
  if request.method == 'GET':
    return render_template('landing.html')

  
#if __name__ == "__main__":
 # app.run(host='0.0.0.0', port=7006, debug=True) 
