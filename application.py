#export FLASK_APP=application.py
#export DATABASE_URL="postgres://ayjxjjxhgpzlnl:f150cc319da46e38a1fb398ee335d98fa5468668d0d8aa3da415aed475d08f9b@ec2-54-225-227-125.compute-1.amazonaws.com:5432/d9prh5mib7dh2p"
#key: 0S6vFxQgJiRIw2CZbc2Yg
# http://exploreflask.com
#secret: 0kmzCjBS62odOXkfg4EcYnoBND3IM28ANuEFlTlWig
#import datetime
from flask import Flask, render_template, request, session, redirect, url_for, send_file # Import the class `Flask` from the `flask` module, written by someone else.
from flask_session import Session
# from flask_mail import Mail, Message
# from flaskext.mail import Mail, Message
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from pprint import pprint
#import csv
import json #for Python to Javascript
import requests #for JSON
import hashlib
from werkzeug.utils import secure_filename


import re

#https://pythonhosted.org/flask-mail/  redo email



app = Flask(__name__) # Instantiate a new web application called `app`, with `__name__` representing the current file
# mail=Mail(app)
UPLOAD_FOLDER = '/static/image'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'housecleanmiami@gmail.com'
app.config['MAIL_PASSWORD'] = 'Brewster1!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# mail = Mail(app)
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session (app)

engine = create_engine("postgres://ayjxjjxhgpzlnl:f150cc319da46e38a1fb398ee335d98fa5468668d0d8aa3da415aed475d08f9b@ec2-54-225-227-125.compute-1.amazonaws.com:5432/d9prh5mib7dh2p")
#talk to datbase wiTh SQL. Object used to manage connections to database.
#Sending data to and from database
db = scoped_session(sessionmaker(bind=engine)) # for individual sessions

#ModuleNotFoundError: No module named 'flask_mail'

#flight = db.execute("SELECT * FROM flights WHERE origin = :origin AND destination = :dest",  {"origin": origin, "dest": destination} ).fetchone()

#db.execute("DELETE FROM flights WHERE origin = :origin", {"origin": origin})
#there's this function encode in postgreSQL
#encode(data bytea, format text)

#so if you have a column named profilePic then it would be like
#encode(profilePic, 'base64')
#db.execute("CREATE TABLE user(id SERIAL PRIMARY KEY, name VARCHAR, email VARCHAR, image BYTEA)")
# db.execute("CREATE TABLE photos1(id SERIAL PRIMARY KEY, image BYTEA(max 30000))")

#db.execute("INSERT INTO photos(image) VALUES (:image)", {"image":image})
# db.execute("CREATE TABLE houseclean4(id SERIAL PRIMARY KEY, name VARCHAR NOT NULL, password VARCHAR NOT NULL, phone VARCHAR NOT NULL UNIQUE, address VARCHAR NOT NULL, latitude FLOAT NOT NULL, longitude FLOAT NOT NULL, email VARCHAR NOT NULL, years SMALLINT NOT NULL,  description VARCHAR NOT NULL, two_hour SMALLINT NOT NULL, three_hour SMALLINT NOT NULL, six_hour SMALLINT NOT NULL ,paid_subscription BOOLEAN, image BYTEA,  broom BOOLEAN NOT NULL,  mop BOOLEAN NOT NULL,  vacuum BOOLEAN NOT NULL,  disinfectant BOOLEAN NOT NULL,  soap_scum BOOLEAN NOT NULL,  tooth_brush BOOLEAN NOT NULL,  scrub_pads BOOLEAN NOT NULL,  sponges BOOLEAN NOT NULL, scraper BOOLEAN NOT NULL,  paper_towels BOOLEAN NOT NULL)")
# db.commit()
# print("dbcreated")
# image = db.execute("SELECT encode(image,'base64') FROM photos LIMIT 1").fetchone()



#select encode(image,'base64') from photos limit 1 ****
# encode(data bytea, format text)

@app.route("/", methods = ["GET"]) # A decorator; when the user goes to the route `/`, exceute the function immediately below
def index():
	houseclean_list=[]
	image_list=[]
	image_string = None
	image = db.execute("SELECT encode(image,'base64') FROM houseclean4").fetchall()
	row_count = db.execute("SELECT COUNT(*) FROM houseclean4").fetchall()
	print("row_count",(row_count[0][0]))
	for i in range(row_count[0][0]):


		print("number",i)
		image_string = "data:image/png;base64," + image[i][0]

		x = re.sub("\n", "", image_string)

		image_list.append(x)
	housecleanDB = db.execute("SELECT * FROM houseclean4").fetchall()
	index=0
	for i in housecleanDB:

		houseclean_data = {
			"name": i.name,
			"phone": i.phone,
			"address": i.address,
			"longitude": i.longitude,
			"latitude": i.latitude,
		    "email": i.email,
			"years": i.years,
			"description": i.description,
			"two_hour": i.two_hour,
			"three_hour": i.three_hour,
			"six_hour": i.six_hour,
			"broom": i.broom,
			"mop": i.mop,
			"disinfectant": i.disinfectant,
		    "vacuum": i.vacuum,
			"soap_scum": i.soap_scum,
			"tooth_brush": i.tooth_brush,
			"scraper": i.scraper,
			"sponges": i.sponges,
			"scrub_pads": i.scrub_pads,
			"paper_towels": i.paper_towels,
			"image": image_list[index]

		 	# "image": 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='

			}
		index=index+1



		houseclean_list.append(houseclean_data)
	# print ("houseclean_data",houseclean_data)
	headline = "Hello Russ"
	# photo = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='
	return render_template("index.html", houseclean_list=houseclean_list, photo=image_list)

@app.route("/signup", methods = ["POST"]) #way to get sign in from index to sign-up page
def signup():
	return render_template("signup.html")

@app.route("/delete_account/<string:phone>", methods = ["POST"]) #way to get sign in from index to sign-up page
def delete_account(phone):

	db.execute("DELETE FROM houseclean4 WHERE phone = :phone", {"phone": phone})
	db.commit()
	session["check_houseclean"] = False
	return redirect(url_for("index"))

@app.route("/sign-in", methods = ["POST"]) #way to get sign in from index to sign-in page
def signin():
	return render_template("sign-in.html")

@app.route("/user", methods = ["POST"]) # user CRUD
def user():
	name = request.form.get("name")
	password1 = request.form.get("password")
	salt = "6Agz"
	db_password = password1+salt
	h = hashlib.md5(db_password.encode())
	password = h.hexdigest()

	if db.execute("SELECT * FROM houseclean4 WHERE name = :name AND password = :password", {"name": name, "password": password}).rowcount == 0:
		return "name and password dont match"
	else:
		user = db.execute("SELECT * FROM houseclean4 WHERE name = :name AND password = :password", {"name": name, "password": password}).fetchall()
	print ("user",user)
	return render_template("user.html", user=user)

@app.route('/ipn/',methods=['POST'])
def ipn():
	arg = ''
	request.parameter_storage_class = ImmutableOrderedMultiDict
	values = request.form
	for x, y in values.iteritems():
		arg += "&{x}={y}".format(x=x,y=y)

	validate_url = 'https://www.paypal.com' \
				   '/cgi-bin/webscr?cmd=_notify-validate{arg}' \
				   .format(arg=arg)
	r = requests.get(validate_url)
	if r.text == 'VERIFIED':
		return redirect(url_for("success"))
	else:
		return "Failure"

@app.route('/success/')
def success():
	return render_template("success.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
	if request.method == 'POST':
		image = request.files['image']
		image_binary = image.read()
		print ("image_binary",image_binary)
		db.execute("INSERT INTO photos(image) VALUES (:image)", {"image":image_binary})
		db.commit()
		return 'file uploaded successfully'

@app.route("/signup_check", methods = ["POST"])
def signup_check():
	imageF = request.files['image']
	image = imageF.read()

	name = request.form.get("name")
	password1 = request.form.get("password")
	salt = "6Agz"
	db_password = password1+salt
	h = hashlib.md5(db_password.encode())
	password = h.hexdigest()
	print("password", password)

	phone1 = request.form.get("phone1")
	phone2 = request.form.get("phone2")
	phone3 = request.form.get("phone3")
	string1 = str(phone1)
	string2 = str(phone2)
	string3 = str(phone3)
	phone=string1+string2+string3

	if db.execute("SELECT * FROM houseclean4 WHERE phone = :phone", {"phone": phone}).rowcount > 0:
		return "Number already taken, please contact support at 786-873-7526"
	street = request.form.get("street")
	city = request.form.get("city")
	state = request.form.get("state")
	zip_code = request.form.get("zip_code")
	email = request.form.get("email")
	years = request.form.get("years")
	description = request.form.get("description")
	two_hour = request.form.get("two_hour")
	three_hour = request.form.get("three_hour")
	six_hour = request.form.get("six_hour")
	broom = request.form.get("broom")
	mop = request.form.get("mop")
	vacuum = request.form.get("vacuum")
	disinfectant = request.form.get("disinfectant")
	soap_scum = request.form.get("soap_scum")
	tooth_brush = request.form.get("tooth_brush")
	scraper = request.form.get("scraper")
	sponges = request.form.get("sponges")
	scrub_pads = request.form.get("scrub_pads")
	paper_towels = request.form.get("paper_towels")

	if broom=="on":
		broom=True
	else:
		broom=False

	if mop=="on":
		mop=True
	else:
		mop=False

	if vacuum=="on":
		vacuum=True
	else:
		vacuum=False

	if disinfectant=="on":
		disinfectant=True
	else:
		disinfectant=False

	if soap_scum=="on":
		soap_scum=True
	else:
		soap_scum=False

	if tooth_brush=="on":
		tooth_brush=True
	else:
		tooth_brush=False

	if scraper=="on":
		scraper=True
	else:
		scraper=False

	if sponges=="on":
		sponges=True
	else:
		sponges=False

	if scrub_pads=="on":
		scrub_pads=True
	else:
		scrub_pads=False

	if paper_towels=="on":
		paper_towels=True
	else:
		paper_towels=False


	address = street+", "+city+", "+state+", "+zip_code
	print(address)

	#geocode
	params = {
		'address': address,
		'key': 'AIzaSyD9fytSdXXr6kVZdXLddFJyF9HT4JTt-qM',
	}
	res = requests.get(GOOGLE_MAPS_API_URL, params=params)
	response = res.json()
	#print("jsonresonse",response)
	latlng=response['results'][0]['geometry']['location']
	latitude = latlng['lat']
	longitude = latlng['lng']
	print("lat", latlng['lat'])
	print("lng", latlng['lng'])

	if session.get("check_houseclean") is True:
		print("check_houseclean=True / cancel upload")
		#return "Please delete account before uploading another"
	else:
		print("check_houseclean=False")


	db.execute("INSERT INTO houseclean4(name, password, phone, address, email, years, latitude, longitude, description, two_hour, three_hour, six_hour, image, broom, mop, vacuum, disinfectant, soap_scum, tooth_brush, scrub_pads, sponges, scraper, paper_towels) VALUES (:name, :password, :phone, :address, :email, :years, :latitude, :longitude, :description, :two_hour, :three_hour, :six_hour, :image, :broom, :mop, :vacuum, :disinfectant, :soap_scum, :tooth_brush, :scrub_pads, :sponges, :scraper, :paper_towels)", {"name":name, "password":password, "phone":phone, "address":address, "email":email, "years":years, "latitude":latitude, "longitude":longitude, "description":description, "two_hour":two_hour, "three_hour":three_hour, "six_hour":six_hour,"image":image, "broom":broom, "mop":mop, "vacuum":vacuum, "disinfectant":disinfectant, "soap_scum":soap_scum, "tooth_brush":tooth_brush, "scrub_pads":scrub_pads, "sponges":sponges, "scraper":scraper, "paper_towels":paper_towels})
	db.commit()
	session["check_houseclean"] = True
	print("check_houseclean=True")
	# msg = Message('Hello From House Cleaning Miami', sender = 'housecleanmiami@gmail.com', recipients = [email])
	# msg.body = 'Hello Testing'
	# mail.send(msg)
	#return "Mail Sent"
	return redirect(url_for("index"))
