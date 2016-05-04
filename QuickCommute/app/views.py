from flask import render_template, request, flash, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from werkzeug.security import generate_password_hash, check_password_hash
#from datetime import datetime
from app import app
import json
import sys
import urllib2
import datetime
import numpy as np

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://websysS16GB6:websysS16GB6!!@websys3/websysS16GB6'
db = SQLAlchemy(app)

lm  = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

@lm.user_loader
def load_user(id):
  return User.query.get(int(id))

class User(db.Model):
  __tablename__ = "UserProfile"
  id = db.Column('UserId', db.Integer, primary_key=True)
  email = db.Column('email', db.String(45), unique=True)
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

class Stations(db.Model):
  __tablename__ = "Stations"
  stationid = db.Column('StationID', db.String(11), primary_key = True)
  stationname = db.Column('StationName', db.String(45))
  BranchID = db.Column('BranchID', db.ForeignKey('Branches.BranchID'))
  
  def __repr__(self):
    return '<Stations %r>' % (self.stationname)

  def __init__(self,stationid,stationname,BranchID):
    this.stationid = stationid
    this.stationname = stationname
    this.BranchID = BranchID

class Branches(db.Model):
  __tablename__ = "Branches"
  BranchID = db.Column('BranchID', db.Integer, primary_key = True)
  branchname = db.Column('BranchName', db.String(45))
  ServiceID = db.Column('ServiceID', db.ForeignKey('Services.ServiceID'))
  def __repr__(self):
    return '<Branches %r>' % (self.branchname)

class Servicess(db.Model):
  __tablename__ = "Services"
  ServiceID = db.Column('ServiceID', db.Integer, primary_key = True)
  servicename = db.Column('ServiceName', db.String(45))
  def __repr__(self):
    return '<Services %r>' % (self.servicename)

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

@app.route('/',methods=['GET','POST'])
def landing():
  if request.method == 'GET':
    return render_template('commuterAppTemplate.html',stations=Stations.query.all())

@app.route('/get_trains', methods = ['GET'])
def get_trains(Service,FROM,TO,HOUR,MIN):
    count = 0
    today = datetime.date.today()
    YEAR = today.year
    MONTH = today.month
    DAY = today.day
    if Service == 'LIRR':
        #urlData = ("https://traintime.lirr.org/api/Departure?api_key=%3CYOUR_KEY%3E&loc={0}".format(FROM))
        urlData = ('https://traintime.lirr.org/api/TrainTime?api_key=%3CYOUR_KEY%3E&startsta={0}&endsta={1}&year={2}&month={3}&day={4}&hour={5}&minute={6}&datoggle=d'.format(FROM,TO,YEAR,MONTH,DAY,HOUR,MIN))
        webUrl = urllib2.urlopen(urlData)
        data = webUrl.read()
        jsonData = json.loads(data)
        Trips = jsonData["TRIPS"]
        #print (len(TrainsData))
        trains = []
        reqtime = int(HOUR) * 100 + int(MIN)
        for trip in Trips:
            legs = trip["LEGS"]
            tripTime = int(legs[0]["DEPART_TIME"])
            if tripTime >= reqtime:
                out_trip = {}
                out_trip["TRAIN_ID"] = legs[0]["TRAIN_ID"]
                out_trip["ETA"] = legs[0]["DEPART_TIME"]
                if legs[0]["TRACK"] == None:
                    out_trip["TRACK"] = "-"
                else:
                    out_trip["TRACK"] = legs[0]["TRACK"]
                trains.append(out_trip)
        output = {}
        output["TRAINS"] = trains
        json_output = json.dumps(output)
    return json_output
  
#if __name__ == "__main__":
 # app.run(host='0.0.0.0', port=7006, debug=True) 
