from flask import request, Flask, render_template, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from joblib import load
import pandas as pd
import numpy as np
import re
import os
import io
import cv2
import tweepy
import time
import mailgenerator
from werkzeug.utils import secure_filename
import pytesseract
from pytesseract import Output
from PIL import Image
import time
import psycopg2
import datetime



label = ['NORMAL' , 'DEPRESSIVE']
BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads")
custom_config = r'--oem 3 --psm 6'
filename = ''


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "abc"

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/depressiondata'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cgyczeola:35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f@ec2-49-89-108-82.compute-2.amazonaws.com:5432/d249ke7abv49ah'

    # "dbname=d249ke7abv49ah host=ec2-49-89-108-82.compute-2.amazonaws.com port=5432 user=cgyczeola password=35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f sslmode=require"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Logins(db.Model):
    __tablename__ = 'logins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text(), unique=True)
    username = db.Column(db.Text())
    password = db.Column(db.Text())

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password


class Register(db.Model):
    __tablename__ = 'register'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text(), unique=True)
    username = db.Column(db.Text())
    password = db.Column(db.Text())
    mobile = db.Column(db.BigInteger)

    def __init__(self, email, username, password, mobile):
        self.email = email
        self.username = username
        self.password = password
        self.mobile = mobile


class Subscribers(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text(), db.ForeignKey('logins.email'))
    tuser = db.Column(db.Text())

    def __init__(self, email, tuser):
        self.email = email
        self.tuser = tuser


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text(),unique=True)
    password = db.Column(db.Text())

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    userx = db.Column(db.Text())
    usery = db.Column(db.Text())
    msg = db.Column(db.Text())
    email = db.Column(db.Text())
    ts = db.Column(db.DateTime)

    def __init__(self, userx, usery, msg, ts):
        self.userx = userx
        self.usery = usery
        self.msg = msg
        self.email = email
        self.ts = ts


class Activemsg(db.Model):
    __tablename__ = 'activemsg'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text(), unique=True)
    auser = db.Column(db.Text())

    def __init__(self, email, auser):
        self.email = email
        self.user = auser


def retrieveUsers():
    try:
        connection = psycopg2.connect(user="cgyczeola", password="35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f", host="ec2-49-89-108-82.compute-2.amazonaws.com", port="5432", database="d249ke7abv49ah")
        cursor = connection.cursor()
        cursor.execute("SELECT id,email,username,mobile,password FROM Register ORDER BY id")
        users=cursor.fetchall()
        cnt=1
        userslist={}
        for i,j,k,l,m in users:
            userslist[cnt]=(j,k,l,m)
            # print(userslist[cnt])
            cnt+=1
        # print(userslist)
        return userslist

    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def resetpass(remail,pwd):
    try:
        connection = psycopg2.connect(user="cgyczeola", password="35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f", host="ec2-49-89-108-82.compute-2.amazonaws.com", port="5432", database="d249ke7abv49ah")
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM Register WHERE email=%s",(remail,))
        user=cursor.fetchone()
        user=user[0]
        # print(user)
        cursor.execute("UPDATE Logins SET password = %s WHERE  username=%s AND email=%s",(pwd,user,remail))
        cursor.execute("UPDATE Register SET password = %s WHERE  username=%s AND email=%s",(pwd,user,remail))
        # print("Reset Successful")
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def changepwd(remail,pwd):
    try:
        connection = psycopg2.connect(user="cgyczeola", password="35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f", host="ec2-49-89-108-82.compute-2.amazonaws.com", port="5432", database="d249ke7abv49ah")
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM Register WHERE email=%s",(remail,))
        user=cursor.fetchone()
        user=user[0]
        cursor.execute("UPDATE Logins SET password = %s WHERE  username=%s AND email=%s",(pwd,user,remail))
        cursor.execute("UPDATE Register SET password = %s WHERE  username=%s AND email=%s",(pwd,user,remail))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def emailcheck(email):
    try:
        connection = psycopg2.connect(user="cgyczeola", password="35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f", host="ec2-49-89-108-82.compute-2.amazonaws.com", port="5432", database="d249ke7abv49ah")
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM Logins WHERE email=%s",(email,))
        res=cursor.fetchone()
        if res is not None:
            return True
        else:
            return False

    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def messages(userx,usery,uemail):
    try:
        connection = psycopg2.connect(user="cgyczeola", password="35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f", host="ec2-49-89-108-82.compute-2.amazonaws.com", port="5432", database="d249ke7abv49ah")
        cursor = connection.cursor()
        # cursor.execute("INSERT INTO Feedback (userx, usery, msg, ts) VALUES (%s,%s,%s,datetime.datetime.now())")
        cursor.execute("SELECT userx,usery,msg,ts FROM Feedback WHERE userx=%s AND usery=%s AND email=%s UNION  SELECT userx,usery,msg,ts FROM Feedback WHERE userx=%s AND usery=%s AND email=%s  ORDER BY ts",(userx,usery,uemail,usery,userx,uemail))
        x = cursor.fetchall()
        message = {}
        cnt=1
        for i,j,k,l in x:
            message[cnt]=(i,j,k)
            cnt+=1
        # print(message)
        return message
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the feedback in database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def addfeed(mfrom,mto,msg,memail):
    try:
        connection = psycopg2.connect(user="cgyczeola", password="35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f", host="ec2-49-89-108-82.compute-2.amazonaws.com", port="5432", database="d249ke7abv49ah")
        cursor = connection.cursor()
        query = "INSERT INTO Feedback (userx, usery, msg, email, ts) VALUES (%s,%s,%s,%s,%s)"
        data = (mfrom, mto, msg, memail, datetime.datetime.now())
        cursor.execute(query, data)
        # print('added to feedback')
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the feedback in database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def addmsg(memail,muser):
    try:
        connection = psycopg2.connect(user="cgyczeola", password="35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f", host="ec2-49-89-108-82.compute-2.amazonaws.com", port="5432", database="d249ke7abv49ah")
        cursor = connection.cursor()
        query = '''INSERT INTO Activemsg (email, auser) VALUES (%s,%s) '''
        # query = """ INSERT INTO Activemsg (email, user) VALUES (%s,%s) """
        data = (memail, muser)
        cursor.execute(query, data)
        # print('added to active list')
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the feedback in database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def delmsg(memail,muser):
    try:
        connection = psycopg2.connect(user="cgyczeola", password="35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f", host="ec2-49-89-108-82.compute-2.amazonaws.com", port="5432", database="d249ke7abv49ah")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Activemsg WHERE email=%s AND auser=%s",(memail,muser))
        # print('deleted from active list')
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the feedback in database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def msgactive():
    try:
        connection = psycopg2.connect(user="cgyczeola", password="35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f", host="ec2-49-89-108-82.compute-2.amazonaws.com", port="5432", database="d249ke7abv49ah")
        cursor = connection.cursor()
        cursor.execute("SELECT email,auser FROM Activemsg")
        x = cursor.fetchall()
        activelist = {}
        cnt=1
        for i,j in x:
            activelist[cnt]=(i,j)
            cnt+=1
        # print(activelist)
        return activelist
        # print('active list')
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the feedback in database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def userList(uemail):
    try:
        connection = psycopg2.connect(user="cgyczeola", password="35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f", host="ec2-49-89-108-82.compute-2.amazonaws.com", port="5432", database="d249ke7abv49ah")
        cursor = connection.cursor()
        cursor.execute("SELECT tuser FROM Subscribers WHERE email=%s",(uemail,))
        users=cursor.fetchall()
        userlist ={}
        cnt=1
        for k in users:
            userlist[cnt]=(k)
            cnt+=1
        return userlist
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def user(uemail):
    try:
        connection = psycopg2.connect(user="cgyczeola", password="35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f", host="ec2-49-89-108-82.compute-2.amazonaws.com", port="5432", database="d249ke7abv49ah")
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM Register WHERE email=%s",(uemail,))
        user=cursor.fetchone()
        user=user[0]
        return user
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def tdelete(uemail,tdname):
    try:
        connection = psycopg2.connect(user="cgyczeola", password="35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f", host="ec2-49-89-108-82.compute-2.amazonaws.com", port="5432", database="d249ke7abv49ah")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Subscribers WHERE email=%s AND tuser=%s",(uemail,tdname))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def tadd(uemail,taname):
    try:
        connection = psycopg2.connect(user="cgyczeola", password="35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f", host="ec2-49-89-108-82.compute-2.amazonaws.com", port="5432", database="d249ke7abv49ah")
        cursor = connection.cursor()
        cursor.execute("SELECT tuser FROM Subscribers WHERE email=%s AND tuser=%s",(uemail,taname))
        check = cursor.fetchone()
        if check:
            return "Twitter User already exists in the list !"
        else:
            cursor.execute("INSERT INTO Subscribers (email,tuser) VALUES (%s,%s)" ,(uemail,taname))
            connection.commit()
            print("Added")
            return "Added Successfully to the list !"
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def rcheck(email,username):
    consumer_key = "Od7zy6m9390gqyUaFomXW9LSv"
    consumer_secret = "IqJYMgtHGaAAUJxzJlsxqgnBKdx8SKP2Q779Kdsz3oEpwQbGde"
    access_token = "1268057362788540416-aUbTXxF5JrRthdcVjXPjZSfTjmJi6n"
    access_token_secret = "Jtzsttach800vnLhAeJPG8UBbOka3v57UsltOcBJAyac0"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    tweets = []
    count = 1
    try:
      tweets = tweepy.Cursor(api.user_timeline,id=username).items(count)
      tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
      tweets_df = pd.DataFrame(tweets_list,columns=['Datetime', 'Tweet Id', 'tweet'])
      tweets_df.to_csv('static/uploads/{}-tweets.csv'.format(username), sep=',', index = False)
    except BaseException as e:
      print('failed on_status,',str(e))
      time.sleep(3)
      # return render_template('t404.html')
      print('Invalid Twitter Username')
      return 'N/A'
    filename='static/uploads/'+username+'-tweets.csv'
    data = pd.read_csv(filename)
    os.remove(filename)
    tweetslist=list(data.values)
    for i in tweetslist:
      m=clean_tweet(i[2])
      if m!='':
          y=analyze(m)
          # print(username,'---->', i[2],'---->',y)
          return y
      else:
          # print(username,'---->',i[2] ,'---->','N/A')
          return 'N/A'


def treports(email):
    try:
        connection = psycopg2.connect(user="cgyczeola", password="35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f", host="ec2-49-89-108-82.compute-2.amazonaws.com", port="5432", database="d249ke7abv49ah")
        cursor = connection.cursor()
        cursor.execute("SELECT email, tuser FROM Subscribers WHERE email=%s",(email,))
        check = cursor.fetchall()
        userlist = []
        for x,y in check:
            userlist.append(y)
        # print(userlist)
        return userlist
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the login table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def temails():
    try:
        connection = psycopg2.connect(user="cgyczeola", password="35a0fda2228912f9d03094dhkjgtlgksmjsnkdlc3f93d4d2cc478ed81ce1759f", host="ec2-49-89-108-82.compute-2.amazonaws.com", port="5432", database="d249ke7abv49ah")
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT email FROM Subscribers")
        emails = cursor.fetchall()
        print(emails)
        # lemails = list(emails)
        # print(lemails, '\n------------')
        lemails = []
        for k in emails:
            lemails.append(k[0])
        print(lemails)
        return lemails

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the login table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def clean_tweet(tweet):
    '''
    Function to clean tweet text by removing links, special characters using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\d+)|(\w+:\/\/\S+)", " ", tweet).split())


def file_detect(data,filename):
    result = []
    for parsed_tweet in data['tweet']:
        ct = clean_tweet(parsed_tweet)
        r=requests.get('https://depression-api.herokuapp.com/predict?'+ct)
        x = json.loads(r.text)
        res = x[1]
        if res == 'Normal':
            li = 0
        else:
            li = 1
        result.append(label[li])

    data['target'] = result
    data = data.replace(0, "Normal")
    data = data.replace(1, "Depressive")
    data.to_csv(r'static/results/'+filename, index=False, header=True)
    return data


def analyze(text):
    r=requests.get('https://depression-api.herokuapp.com/predict?'+text)
    x = json.loads(r.text)
    res = x[1]
    if res == 'Normal':
        li = 0
    else:
        li = 1
    return label[li]


@app.route('/')
def home():
    text = ''
    r=requests.get('https://depression-api.herokuapp.com/predict?'+text)
    return render_template('home.html')


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


@app.route('/userlogin')
def userloginpage():
    return render_template('userlogin.html')

@app.route('/userlogin',methods=['POST','GET'])
def userlogin():
    if request.method=='POST' and 'useremail' in request.form and 'password' in request.form:
        useremail=request.form['useremail'].strip()
        pwd=request.form['password'].strip()
        login = Logins.query.filter_by(email = useremail, password=pwd).first()
        if login:
            # print(login)
            session['loggedin'] = True
            session['email'] = login.email
            session['username'] = login.username
            session['password'] = login.password
            if session['loggedin']:
                # return render_template('selection.html',user=session['username'])
                return redirect(url_for('select',user=session['username']))
            else:
                return render_template('userlogin.html')
        else:
            return render_template('userlogin.html',info='Invalid Email or Password!')
    else:
        return render_template('userlogin.html')


@ app.route('/logout')
def logout():
    # remove the username from the session if it is there
    if session['loggedin']:
        session['loggedin'] = False
        # session.pop('loggedin', None)
        session.pop('username', None)
        session.pop('email', None)
        session.pop('password', None)
        # return render_template('userlogin.html')
        return redirect('userlogin')
    else:
        return redirect('userlogin')

@ app.route('/alogout')
def alogout():
    # remove the username from the session if it is there
    if session['aloggedin']:
        session['aloggedin'] = False
        # session.pop('aloggedin', None)
        session.pop('ausername', None)
        return redirect('adminlogin')
    else:
        return redirect('adminlogin')

@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method=='POST':
        username=request.form['username'].strip()
        password=request.form['password'].strip()
        email=request.form['email'].strip()
        phone=request.form['phone']
        # echeck=dbHandler.regemail(email)
        # ucheck=dbHandler.reguser(username)
        dup = Register.query.filter_by(email=email).first()
        if dup is not None:
            return render_template('register.html',info='Email already exists!')
        else:
            x=[]
            session['ruser'] = username
            session['rpass'] = password
            session['remail'] = email
            session['rnum'] = phone
            x.append(email)
            session['rotp'] = mailgenerator.Sending_report(x)
            return render_template('mailverification.html', email=email)
    else:
        return render_template('register.html')


@app.route('/adminlogin')
def adminloginpage():
    return render_template('adminlogin.html')


@app.route('/adminlogin',methods=['POST','GET'])
def adminlogin():
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username'].strip()
        password=request.form['password'].strip()
        login = Admin.query.filter_by(username = username, password = password).first()
        if login:
            # print(login)
            session['aloggedin'] = True
            session['ausername'] = login.username
            # x = retrieveUsers()
            # return render_template('adminview.html',user=username,userslist=x)
            return redirect('adminview')
        else:
            return render_template('adminlogin.html',info='Invalid Credentials')
    else:
        return render_template('adminlogin.html',info='Invalid Credentials')


@app.route('/select')
def select():
    if session['loggedin']:
        # print(session['loggedin'])
        exp = 'format+.csv'
        dir = 'static/uploads'
        try:
            for f in os.listdir(dir):
                if f != exp:
                    os.remove(os.path.join(dir, f))
        except:
            print(dir)
            print('The folder is empty')
        dir = 'static/results'

        try:
            for f in os.listdir(dir):
                if f != exp:
                    os.remove(os.path.join(dir, f))
        except:
            print(dir)
            print('The folder is empty')

        return render_template('selection.html' , user=session['username'])
    else:
        return redirect('userlogin')


@app.route('/mailverification', methods=['GET','POST'])
def mailverification():
    if request.method=='POST':
        motp=request.form['vemail'].strip()
        motp=int(motp)
        if session['rotp']==motp:
            # dbHandler.insertUser(ruser,rpass,remail,rnum)
            register = Register(email=session['remail'], username=session['ruser'], password=session['rpass'], mobile=session['rnum'])
            db.session.add(register)
            login = Logins(email=session['remail'], username=session['ruser'], password=session['rpass'])
            db.session.add(login)
            db.session.commit()
            session.pop('remail',None)
            session.pop('ruser',None)
            session.pop('rpass',None)
            session.pop('rnum',None)
            session.pop('rotp',None)
            return render_template('register.html' ,info='Registeration Successful!')
        else:
            return render_template('mailverification.html' ,email=session['remail'], info='Wrong OTP')
    else:
        return render_template('userlogin.html')


@app.route('/passmail')
def mailpage():
    return render_template('passmail.html')

@app.route('/passmail', methods=['GET','POST'])
def passmail():
    if request.method=='POST':
        email=request.form['email'].strip()
        x=[]
        # global remail
        res = emailcheck(email)
        if res:
            x.append(email)
            session['otp'] = mailgenerator.Sending_report(x)
            # remail = email
            session['email'] = email
            return render_template('passreset.html' ,email=email)
        else:
            x = "You don't have an account"
            return render_template('passmail.html', info = x )
    else:
        return render_template('userlogin.html')



@app.route('/passreset')
def resetpage():
    return render_template('passreset.html')


@app.route('/changepass')
def changepage():
    if session['loggedin']:
        return render_template('changepass.html')
    else:
        return render_template('userlogin.html')


@app.route('/passreset', methods=['GET','POST'])
def passreset():
    if request.method=='POST':
        motp=request.form['vemail'].strip()
        password=request.form['password'].strip()
        cpass=request.form['cpass'].strip()
        # global remail
        remail = session['email']
        motp=int(motp)
        if session['otp'] ==motp and password==cpass:
            resetpass(remail,password)
            otp = 'xxxxxx'
            session.pop('email', None)
            session.pop('otp', None)
            return render_template('userlogin.html' ,info='Password Reset Successful!')
        elif otp!=motp:
            return render_template('passreset.html' ,info='Wrong OTP')
        elif password!=cpass:
            return render_template('passreset.html' ,info='Check your password again')
    else:
        return render_template('passreset.html')


@app.route('/changepass', methods=['GET','POST'])
def changepass():
    if request.method=='POST' and session['loggedin']:
        email=request.form['email'].strip()
        password=request.form['password'].strip()
        cpass=request.form['cpass'].strip()
        if session['email']==email and password==cpass:
            changepwd(email,password)
            return render_template('changepass.html', info="Password updated successfully!")
        elif session['email']!=email:
            return render_template('changepass.html', info="Wrong mail id")
        elif password!=cpass:
            return render_template('changepass.html', info="Check your password again")
    else:
        return redirect('userlogin')


@app.route('/adminview')
def adminview():
    if session['aloggedin']:
        x=retrieveUsers()
        return render_template('adminview.html',user=session['ausername'],userslist=x)
    else:
        return redirect('adminlogin')


@app.route('/feedback')
def feedback():
    if session['loggedin']:
        x = messages('Sarath Majji', session['username'], session['email'])
        return render_template('feedback.html', message = x)
    else:
        return redirect('userlogin')

@app.route('/feedmsg', methods=['GET','POST'])
def feedmsg():
    if request.method=='POST' and session['loggedin']:
        text = request.form['dtext'].strip()
        addfeed(session['username'],'Sarath Majji', text, session['email'])
        addmsg(session['email'],session['username'])
        # x = messages('Sarath Majji', session['username'])
        # print('***********')
        return redirect('feedback')
    else:
        # print('-------------')
        return redirect('userlogin')


@app.route('/afeedback/<user>/<uemail>')
def afeedback(user,uemail):
    if session['aloggedin']:
        x = messages('Sarath Majji', user, uemail)
        session['feeduser'] = user
        session['feedemail'] = uemail
        delmsg(uemail,user)
        return render_template('adminfeedback.html', message = x)
    else:
        return redirect('adminlogin')

@app.route('/active')
def active():
    if session['aloggedin']:
        x = msgactive()
        return render_template('activemsg.html', userslist = x, user = session['ausername'] )
    else:
        return redirect('adminlogin')


@app.route('/afeeds')
def afeeds():
    if session['aloggedin']:
        x = messages('Sarath Majji',session['feeduser'], session['feedemail'])
        return render_template('adminfeedback.html', message = x)
    else:
        return redirect('adminlogin')


@app.route('/afeedmsg', methods=['GET','POST'])
def afeedmsg():
    if request.method=='POST' and session['aloggedin']:
        text = request.form['dtext'].strip()
        addfeed('Sarath Majji',session['feeduser'] ,text, session['feedemail'])
        # x = messages('Sarath Majji', session['username'])
        # print('***********')
        return redirect(url_for('afeedback',user = session['feeduser'], uemail = session['feedemail']))
    else:
        # print('-------------')
        return redirect('adminlogin')


@app.route('/susers/<useremail>')
def susers(useremail):
    if session['aloggedin']:
        x = userList(useremail)
        u = user(useremail)
        return render_template('susers.html', admin = session['ausername'], userlist = x, user = u)
    else:
        return redirect('adminlogin')


@app.route('/predict')
def text_page():
    if session['loggedin']:
        return render_template('index.html')
    else:
        return render_template('userlogin.html')


@app.route('/predict' , methods=['POST'])
def predict():
    if session['loggedin']:
        text = request.form['dtext'].strip()
        otext = text
        text = text.lower()
        text = clean_tweet(text)
        r=requests.get('https://depression-api.herokuapp.com/predict?'+text)
        x = json.loads(r.text)
        res = x[1]
        if res == 'Normal':
            li = 0
        else:
            li = 1
        return render_template('index.html' , prediction_text = label[li], index = li, text = otext)
    else:
        return redirect('userlogin')


@app.route('/file_upload')
def file_upload():
    if session['loggedin']:
        return render_template('ufile.html')
    else:
        return render_template('userlogin.html')

@app.route('/file_predict', methods=['POST'])
def file_predict():
    if request.method == "POST" and session['loggedin']:
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df = pd.read_csv(file_path)
        try:
            result=file_detect(df,filename)
            return render_template('ufile.html', tables=[result.to_html(classes='data')], titles=result.columns, file = filename)
        except:
            return render_template('f404.html')
    else:
        return redirect('userlogin')



@app.route('/twitter',methods=['GET','POST'])
def twitter():
    if session['loggedin']:
        return render_template('twitter.html')
    else:
        return render_template('userlogin.html')

@app.route('/tweets', methods=['POST'])
def tweets():
    if session['loggedin']:
        username=request.form['username'].strip()
        #print(username)
        consumer_key = "Od7zy6m9390gqyUaFomXW9LSv"
        consumer_secret = "IqJYMgtHGaAAUJxzJlsxqgnBKdx8SKP2Q779Kdsz3oEpwQbGde"
        access_token = "1268057362788540416-aUbTXxF5JrRthdcVjXPjZSfTjmJi6n"
        access_token_secret = "Jtzsttach800vnLhAeJPG8UBbOka3v57UsltOcBJAyac0"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth,wait_on_rate_limit=True)
        tweets = []
        count = 10
        try:
            tweets = tweepy.Cursor(api.user_timeline,id=username).items(count)
            tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
            tweets_df = pd.DataFrame(tweets_list,columns=['Datetime', 'Tweet Id', 'tweet'])
            tweets_df.to_csv('static/uploads/{}-tweets.csv'.format(username), sep=',', index = False)
        except BaseException as e:
            print('failed on_status,',str(e))
            time.sleep(3)
            return render_template('t404.html')
        x=[]
        a={}
        result = []
        clean = []
        filename='static/uploads/'+username+'-tweets.csv'
        data = pd.read_csv(filename)
        tweetslist=list(data.values)
        n=0
        d=0
        for i in tweetslist:
            m=clean_tweet(i[2])
            clean.append(m)
            if m!='':
                x.append(m)
                y=analyze(m)
                result.append(y)
                a[i[2]]=y
                if y=='NORMAL':
                    n+=1
                elif y=='DEPRESSIVE':
                    d+=1
            else:
                result.append('N/A')
                a[i[2]]='N/A'
        data['target'] = result
        data['clean tweet'] = clean
        data = data.replace(0, "Normal")
        data = data.replace(1, "Depressive")
        data.to_csv(r'static/results/'+username+'-tweets.csv', index=False, header=True)
        try:
            npercent=(n/(n+d))*100
        except:
            npercent=0
        try:
            dpercent=(d/(n+d))*100
        except:
            dpercent=0

        return render_template('twitter1.html',tweetslist=a,npercent=round(npercent,1),dpercent=round(dpercent,1), file = username+'-tweets.csv', name = username)
    else:
        return redirect('userlogin')

@app.route('/utweets/<tusername>')
def utweets(tusername):
    if session['loggedin']:
        username = tusername
        consumer_key = "Od7zy6m9390gqyUaFomXW9LSv"
        consumer_secret = "IqJYMgtHGaAAUJxzJlsxqgnBKdx8SKP2Q779Kdsz3oEpwQbGde"
        access_token = "1268057362788540416-aUbTXxF5JrRthdcVjXPjZSfTjmJi6n"
        access_token_secret = "Jtzsttach800vnLhAeJPG8UBbOka3v57UsltOcBJAyac0"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth,wait_on_rate_limit=True)
        tweets = []
        count = 10
        try:
            tweets = tweepy.Cursor(api.user_timeline,id=username).items(count)
            tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
            tweets_df = pd.DataFrame(tweets_list,columns=['Datetime', 'Tweet Id', 'tweet'])
            tweets_df.to_csv('static/uploads/{}-tweets.csv'.format(username), sep=',', index = False)
        except BaseException as e:
            print('failed on_status,',str(e))
            time.sleep(3)
            return render_template('t404.html')
        x=[]
        a={}
        result = []
        clean = []
        filename='static/uploads/'+username+'-tweets.csv'
        data = pd.read_csv(filename)
        tweetslist=list(data.values)
        n=0
        d=0
        for i in tweetslist:
            m=clean_tweet(i[2])
            clean.append(m)
            if m!='':
                x.append(m)
                y=analyze(m)
                result.append(y)
                a[i[2]]=y
                if y=='NORMAL':
                    n+=1
                elif y=='DEPRESSIVE':
                    d+=1
            else:
                result.append('N/A')
                a[i[2]]='N/A'
        data['target'] = result
        data['clean tweet'] = clean
        data = data.replace(0, "Normal")
        data = data.replace(1, "Depressive")
        data.to_csv(r'static/results/'+username+'-tweets.csv', index=False, header=True)
        try:
            npercent=(n/(n+d))*100
        except:
            npercent=0
        try:
            dpercent=(d/(n+d))*100
        except:
            dpercent=0
        return render_template('twitter1.html',tweetslist=a,npercent=round(npercent,1),dpercent=round(dpercent,1), file = username+'-tweets.csv', name = username)
    else:
        return redirect('userlogin')


@app.route('/subscribers')
def subpage():
    if session['loggedin']:
        x = userList(session['email'])
        return render_template('subscribers.html', user = session['username'], userlist = x)
    else:
        return redirect('userlogin')


@app.route('/utdelete/<tusername>')
def utdelete(tusername):
    if session['loggedin']:
        x = tdelete(session['email'],tusername)
        x = userList(session['email'])
        return render_template('subscribers.html', user = session['username'], userlist = x)
    else:
        return redirect('userlogin')

@app.route('/utadd/<tusername>')
def utadd(tusername):
    if session['loggedin']:
        consumer_key = "Od7zy6m9390gqyUaFomXW9LSv"
        consumer_secret = "IqJYMgtHGaAAUJxzJlsxqgnBKdx8SKP2Q779Kdsz3oEpwQbGde"
        access_token = "1268057362788540416-aUbTXxF5JrRthdcVjXPjZSfTjmJi6n"
        access_token_secret = "Jtzsttach800vnLhAeJPG8UBbOka3v57UsltOcBJAyac0"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth,wait_on_rate_limit=True)
        tweets = []
        count = 10
        try:
            tweets = tweepy.Cursor(api.user_timeline,id=tusername).items(count)
            tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
            tweets_df = pd.DataFrame(tweets_list,columns=['Datetime', 'Tweet Id', 'tweet'])
            # print(tweets_df)
            if not tweets_df.empty:
                info = tadd(session['email'],tusername)
                if info == 'Added Successfully to the list !':
                    x = userList(session['email'])
                    return render_template('subscribers.html', user = session['username'], userlist = x, msg = info)
                else:
                    x = userList(session['email'])
                    return render_template('subscribers.html', user = session['username'], userlist = x, msg = info)
            else:
                return render_template('t404.html')
        except BaseException as e:
            print('failed on_status,',str(e))
            time.sleep(3)
            return render_template('t404.html')
    else:
        return redirect('userlogin')

@app.route('/image')
def image():
    if session['loggedin']:
        return render_template('picture.html')
    else:
        return render_template('userlogin.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == "POST" and session['loggedin']:
        # img = request.files['file'].read()
        file = request.files['file']
        if file:
            global filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        scanned_text = pytesseract.image_to_string(Image.open(file))
        t=''
        d = pytesseract.image_to_data(Image.open(file), config=custom_config,output_type=Output.DICT)
        # print(d.keys())
        # print(d['text'])
        n_boxes = len(d['text'])
        _img = cv2.imread('static/uploads/'+filename)
        for i in range(n_boxes):
            if len(d['text'][i]) > 1:
                t=t+' '+d['text'][i]
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                _img = cv2.rectangle(_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imwrite('static/uploads/'+filename , _img)
        res = analyze(t)
        if res == "NORMAL":
            color = 'green'
        else:
            color = 'red'
        return render_template('display.html' ,text = scanned_text , result = res, file = filename, col = color)
    else:
        return redirect('userlogin')


@app.route('/report', methods=['POST','GET'])
def report():
    reportdict = {}
    elist = temails()
    # print('***********', elist, len(elist))
    for k in elist:
        x = treports(k)
        print(x)
        ulist = []
        f=0
        for t in x:
            r = rcheck(k,t)
            if r == 'DEPRESSIVE':
                f=1
                ulist.append(t)
        if f==1:
            reportdict[k] = ulist

    return jsonify(reportdict)





if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r'/app/.apt/usr/share/tesseract-ocr/4.00/tessdata'
    app.run()
