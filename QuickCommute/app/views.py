from flask import jsonify, render_template, request, flash, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from werkzeug.security import generate_password_hash, check_password_hash
import time
from app import app
from datetime import datetime
#from mysql.connector import (connection)
import MySQLdb
import json
import sys
import urllib2
import numpy as np
import pandas as pd
from crossdomain import crossdomain
from flask.ext.cors import CORS, cross_origin
from xml.etree import cElementTree as ET

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://websysS16GB6:websysS16GB6!!@websys3/websysS16GB6'
db = SQLAlchemy(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

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
  name = db.Column('Name', db.String(45))
  password = db.Column('Password', db.String(128))
  registration_time = db.Column('RegistrationTime', db.DateTime)
    
  def __init__(self, email, name, password):
    self.email = email
    self.set_password(password)
    self.name = name
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

class Services(db.Model):
  __tablename__ = "Services"
  ServiceID = db.Column('ServiceID', db.Integer, primary_key = True)
  servicename = db.Column('ServiceName', db.String(45))
  def __repr__(self):
    return '<Services %r>' % (self.servicename)

db.create_all()

@app.route('/register', methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def register():
  if request.method == 'GET':
    return render_template('register.html')
  name = request.form['text-basic']
  print name
  email = request.form['email']
  password = request.form['password']
  print email
  user = User(email,name,password)
  db.session.add(user)
  db.session.commit()
  flash('User registered successfully!!')
  return jsonify({ 'email': email, 'status' : 'success' }), 201

@app.route('/login', methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
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
    return json.dumps({'status':'success'}), 201
  else:
    flash('Email or password is invalid', 'error')
    return json.dumps({"status":"failure", "message": "invalid password"}), 201

@app.route('/',methods=['GET','POST'])
def landing():
  if request.method == 'GET':
    return render_template('commuterAppTemplate.html')

@app.route('/GetStationName',methods = ['GET'])
def GetStationName(StationID1,StationID2):
    db = MySQLdb.connect(user='websysS16GB6', password='websysS16GB6!!',host='websys3.stern.nyu.edu',database = 'websysS16GB6')
    cursor1 = db.cursor()
    select_station1 = "SELECT StationName FROM Stations WHERE StationID = '%s'"%(StationID1)
    cursor1.execute(select_station1)
    St1 = cursor1.fetchone()
    cursor1.close()
    cursor2 = db.cursor()
    select_station2 = "SELECT StationName FROM Stations WHERE StationID = '%s'"%(StationID2)
    cursor2.execute(select_station2)
    St2 = cursor2.fetchone()
    cursor2.close()
    db.close()
    return St1[0], St2[0]

@app.route('/GetStationsFrom', methods = ['GET','POST'])
def GetStationsFrom(ServiceID,Char):
    db = MySQLdb.connect(user='websysS16GB6', password='websysS16GB6!!',host='websys3.stern.nyu.edu',database = 'websysS16GB6')
    cursor = db.cursor()
    select_station = ("SELECT S.ServiceID,\
                              S.StationID,\
                              S.StationName,\
                              CASE S.StationID\
                                  WHEN 'TS' THEN 'Secaucus Lower Level'\
                                  WHEN 'SE' THEN 'Secaucus Upper Level'\
                                  ELSE S.StationName\
                              END AS DisplayName\
                         FROM Stations S,\
                              Services V\
                        WHERE S.ServiceID = V.ServiceID AND\
                              V.ServiceID = %s AND\
                              UPPER(S.StationName) LIKE '%s'")%(ServiceID,"%"+Char.upper()+"%")
    cursor.execute(select_station)
    Stations = []
    for ServiceID, StationID, StationName, DisplayName in cursor:
        Station={}
        Station["ServiceID"] = ServiceID
        Station["StationID"] = StationID
        Station["StationName"] = StationName
        Station["DisplayName"] = DisplayName
        Stations.append(Station)
    Stations_Out = {}
    Stations_Out["Stations"] = Stations
    json_output = json.dumps(Stations_Out)
    cursor.close()
    db.close()
    return json_output

@app.route('/GetStationsTo', methods = ['GET','POST'])
def GetStationsTo(ServID,StatID):
    db = MySQLdb.connect(user='websysS16GB6', password='websysS16GB6!!',host='websys3.stern.nyu.edu',database = 'websysS16GB6')
    cursor = db.cursor()
    if StatID in ('TS','SE'):
        StID = "TS','SE"
    else:
        StID = StatID
    select_station = ("\
       SELECT S.ServiceID,\
              S.StationID,\
              CASE S.StationID\
                  WHEN 'TS' THEN CONCAT('Secaucus Lower Level : ',S.BranchesName)\
                  WHEN 'SE' THEN CONCAT('Secaucus Upper Level : ',S.BranchesName)\
                  ELSE  CONCAT(S.StationName,' : ',S.BranchesName)\
              END AS DisplayName,\
              S.StationName\
         FROM (  SELECT SB.ServiceID,\
                        SB.StationID,\
                        GROUP_CONCAT(DISTINCT B.BranchName ORDER BY B.BranchID DESC SEPARATOR ' - ') AS BranchesName,\
                        S.StationName\
                   FROM STATIONBRANCH SB,\
                        Stations S,\
                        Branches B\
                  WHERE SB.ServiceID = S.ServiceID AND\
                        SB.StationID = S.StationID AND\
                        SB.ServiceID = B.ServiceID AND\
                        SB.BranchID  = B.BranchID  AND\
                        SB.StationID NOT IN ('{1}') AND\
                        (SB.ServiceID,SB.BranchID) IN (  SELECT SB1.ServiceID,SB1.BranchID\
                                                           FROM STATIONBRANCH SB1\
                                                          WHERE SB1.ServiceID = '{0}' AND\
                                                                SB1.StationID IN ('{1}'))\
               GROUP BY SB.ServiceID,SB.StationID,S.StationName) S\
    ORDER BY S.StationName;").format(ServID,StID)
    cursor.execute(select_station)
    Stations = []
    for ServiceID, StationID, DisplayName, StationName in cursor:
        Station={}
        Station["ServiceID"] = ServiceID
        Station["StationID"] = StationID
        Station["DisplayName"] = DisplayName
        Station["StationName"] = StationName
        Stations.append(Station)
    Stations_Out = {}
    Stations_Out["Stations"] = Stations
    json_output = json.dumps(Stations_Out)
    cursor.close()
    db.close()
    return json_output

@app.route('/GetTrains', methods = ['GET','POST'])
def GetTrains(Service,FROM,TO,HOUR,MIN):
    count = 0
    today = datetime.date.today()
    YEAR = today.year
    MONTH = today.month
    DAY = today.day
    trains = []
    reqtime = datetime.datetime(YEAR,MONTH,DAY,int(HOUR),int(MIN))
    if Service == 'LIRR':
        urlData = ('https://traintime.lirr.org/api/TrainTime?api_key=%3CYOUR_KEY%3E&startsta={0}&endsta={1}&year={2}&month={3}&day={4}&hour={5}&minute={6}&datoggle=d'.format(FROM,TO,YEAR,MONTH,DAY,HOUR,MIN))
        webUrl = urllib2.urlopen(urlData)
        data = webUrl.read()
        jsonData = json.loads(data)
        Trips = jsonData["TRIPS"]
        for trip in Trips:
            legs = trip["LEGS"]
            tripTime = datetime.datetime.strptime(trip["ROUTE_DATE"]+legs[0]["DEPART_TIME"],"%Y%m%d%H%M")
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
    elif Service == 'NJT':
        FROMName,TOName = GetStationName(FROM,TO)
        username = 'aporcel'
        #password = 'S2PC4VhL3JgE7W'
        password = 'OTBhV18N3O66ZL'
        request = urllib2.Request("http://traindata.njtransit.com:8092/NJTTrainData.asmx/getTrainScheduleJSON?username={0}&password={1}&station={2}".format(username,password,FROM))
        result = urllib2.urlopen(request)
        xmlstr = result.read()
        root = ET.fromstring(xmlstr)
        jdata = json.loads(root.text)
        Trips = jdata["STATION"]["ITEMS"]["ITEM"]
        for trip in Trips:
            stops = trip["STOPS"]
            tripTime = datetime.datetime.strptime(trip["SCHED_DEP_DATE"],"%d-%b-%Y %I:%M:%S %p")
            IsInStop = False
            if isinstance(stops["STOP"],dict):
                IsInStop = stops["STOP"]["NAME"] == TOName
            else:
                FlagCheckTO = False
                for stop in stops["STOP"]:
                    if FROMName == stop["NAME"]:
                        FlagCheckTO = True
                    if FlagCheckTO & (TOName == stop["NAME"]):
                        IsInStop = True
                        break
            if IsInStop & (tripTime >= reqtime):
                out_trip = {}
                out_trip["TRAIN_ID"] = trip["TRAIN_ID"]
                out_trip["ETA"] = trip["SCHED_DEP_DATE"]
                if (trip["TRACK"] == None) | (trip["TRACK"] == ""):
                    out_trip["TRACK"] = "-"
                else:
                    out_trip["TRACK"] = trip["TRACK"]
                trains.append(out_trip)
        output = {}
        output["TRAINS"] = trains
        json_output = json.dumps(output)     
    return json_output

#if __name__ == "__main__":
 # app.run(host='0.0.0.0', port=7006, debug=True) 
