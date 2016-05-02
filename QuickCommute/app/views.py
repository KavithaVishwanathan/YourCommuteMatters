from flask import render_template
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from datetime import datetime
from app import app

@app.route('/')
@app.route('/index')
def index():
  return "Hello, World!"

lm  = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

@lm.user_loader
def load_user(id):
  return User.query.get(int(id))

class User(db.Model):
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
    self.registered_time = datetime.estnow()
 
  def set_password(self,password):
    self.password = generate_password_has(password)

  def check_password(self, password):
    return check_password_has(self.password,password)

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

  registered_user = User.query.filter_by(username=username).first()
  flash(registered_user.check_password(registered_user.password))

  
  
  
