#export FLASK_APP=application.py
#export DATABASE_URL="postgres://ayjxjjxhgpzlnl:f150cc319da46e38a1fb398ee335d98fa5468668d0d8aa3da415aed475d08f9b@ec2-54-225-227-125.compute-1.amazonaws.com:5432/d9prh5mib7dh2p"
#key: 0S6vFxQgJiRIw2CZbc2Yg
# http://exploreflask.com  #https://pythonhosted.org/flask-mail/  redo email
#secret: 0kmzCjBS62odOXkfg4EcYnoBND3IM28ANuEFlTlWig
#import datetime
# https://flask-bcrypt.readthedocs.io/en/latest/
from flask import Flask, render_template, request, session, redirect, url_for, send_file # Import the class `Flask` from the `flask` module, written by someone else.
from flask_session import Session
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import json #for Python to Javascript
import requests #for JSON
import hashlib #password
import re  #regex

# from flask_talisman import Talisman # https  use this instead SSLify
# from flask_seasurf import SeaSurf # goes with talisman

app = Flask(__name__) # Instantiate a new web application called `app`, with `__name__` representing the current file
# Talisman(app)

UPLOAD_FOLDER = '/static/image'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'housecleanmiami@gmail.com'
app.config['MAIL_PASSWORD'] = 'Brewster1!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
from flask_sslify import SSLify
sslify = SSLify(app, age=300)
# csrf = SeaSurf(app)  # protection
Session (app)
engine = create_engine("postgres://ayjxjjxhgpzlnl:f150cc319da46e38a1fb398ee335d98fa5468668d0d8aa3da415aed475d08f9b@ec2-54-225-227-125.compute-1.amazonaws.com:5432/d9prh5mib7dh2p")
#talk to datbase wiTh SQL. Object used to manage connections to database.
#Sending data to and from database
db = scoped_session(sessionmaker(bind=engine)) # for individual sessions



#flight = db.execute("SELECT * FROM flights WHERE origin = :origin AND destination = :dest",  {"origin": origin, "dest": destination} ).fetchone()

#db.execute("DELETE FROM flights WHERE origin = :origin", {"origin": origin})
#there's this function encode in postgreSQL
#encode(data bytea, format text)

#so if you have a column named profilePic then it would be like
#encode(profilePic, 'base64')
#db.execute("CREATE TABLE user(id SERIAL PRIMARY KEY, name VARCHAR, email VARCHAR, image BYTEA)")
# db.execute("CREATE TABLE photos1(id SERIAL PRIMARY KEY, image BYTEA(max 30000))")
# db.execute("INSERT INTO houseclean7 (studio) WHERE id = 5 VALUES (90)")
# db.execute("INSERT INTO photos(image) VALUES (:image)", {"image":image})
# db.execute("CREATE TABLE houseclean7(id SERIAL PRIMARY KEY, name VARCHAR NOT NULL, password VARCHAR NOT NULL, phone VARCHAR NOT NULL UNIQUE, address VARCHAR NOT NULL, latitude FLOAT NOT NULL, longitude FLOAT NOT NULL, email VARCHAR NOT NULL, years SMALLINT NOT NULL,  description VARCHAR NOT NULL, hourly_rate SMALLINT, numcleaners SMALLINT, studio SMALLINT, one_bed SMALLINT, two_bed SMALLINT, three_bed SMALLINT, deep_clean SMALLINT, paid_subscription BOOLEAN, image BYTEA,  broom BOOLEAN NOT NULL,  mop BOOLEAN NOT NULL,  vacuum BOOLEAN NOT NULL,  disinfectant BOOLEAN NOT NULL,  soap_scum BOOLEAN NOT NULL,  tooth_brush BOOLEAN NOT NULL,  scrub_pads BOOLEAN NOT NULL,  sponges BOOLEAN NOT NULL, scraper BOOLEAN NOT NULL,  paper_towels BOOLEAN NOT NULL)")
# db.commit()
# print("dbcreated")
# image = db.execute("SELECT encode(image,'base64') FROM photos LIMIT 1").fetchone()



#select encode(image,'base64') from photos limit 1 ****
# encode(data bytea, format text)

@app.route("/", methods = ['GET',"POST"]) # A decorator; when the user goes to the route `/`, exceute the function immediately below
def index():

	houseclean_list=[]
	image_list=[]
	image_string = ""
	# image = db.execute("SELECT encode(image,'base64') FROM houseclean7").fetchall()
	# row_count = db.execute("SELECT COUNT(*) FROM houseclean7").fetchall()

	# for i in range(row_count[0][0]):
		# image_string = "data:image/png;base64," + image[i][0]
		# x = re.sub("\n", "", image_string)
		# image_list.append(x)

	housecleanDB = db.execute("SELECT * FROM houseclean7 ").fetchall()
	# print (housecleanDB)
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
			"hourly_rate": i.hourly_rate,
			"numcleaners": i.numcleaners,
			"studio": i.studio,
			"one_bed": i.one_bed,
			"two_bed": i.two_bed,
			"three_bed": i.three_bed,
			"deep_clean": i.deep_clean,
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
			# "image": image_list[index]
			}
		index=index+1
		houseclean_list.append(houseclean_data)
		# print ("houseclean_data",houseclean_data["description"])
	return render_template("index.html", houseclean_list=houseclean_list )

@app.route("/sign-up", methods = ['GET',"POST"]) #way to get sign in from index to sign-up page
def signup():
	return render_template("signup.html")

@app.route("/delete_account/<string:phone>", methods = ["POST"]) #way to get sign in from index to sign-up page
def delete_account(phone):

	db.execute("DELETE FROM houseclean7 WHERE phone = :phone", {"phone": phone})
	db.commit()
	session["check_houseclean"] = False
	return redirect(url_for("index"))

@app.route("/sign-in", methods = ["POST"]) #way to get sign in from index to sign-in page
def signin():
	return render_template("sign-in.html")

@app.route("/about", methods = ['GET',"POST"]) #way to get sign in from index to sign-in page
def about():
	return render_template("about.html")

@app.route("/blog-page", methods = ['GET',"POST"]) #way to get sign in from index to sign-in page
def blogpage():
	return render_template("blogpage.html")

@app.route("/house_cleaning_blog/", methods = ['GET',"POST"]) #way to get sign in from index to sign-in page
def house_cleaning_blog():
	return render_template("blog.html")

@app.route('/background_process_test/<string:phone>')
def background_process_test(phone):
    print ("Hello", phone)
    return "nothing"


@app.route("/blog/<int:year>/<int:month>/<int:day>/<string:title>", methods = ['GET',"POST"]) #way to get sign in from index to sign-in page
def blog(year,month,day,title):
	if title == "Price-Service-Location":
		return render_template("blog.html")
	elif title == "Cuban-Mop":
		return render_template("blog2.html")
	else:
		return render_template("blog.html")

@app.route("/user", methods = ["POST"]) # user CRUD
def user():
	name = request.form.get("name")
	password1 = request.form.get("password")
	salt = "6Agz"
	db_password = password1+salt
	h = hashlib.md5(db_password.encode())
	password = h.hexdigest()

	if db.execute("SELECT * FROM houseclean7 WHERE name = :name AND password = :password", {"name": name, "password": password}).rowcount == 0:
		return "name and password dont match"
	else:
		user = db.execute("SELECT * FROM houseclean7 WHERE name = :name AND password = :password", {"name": name, "password": password}).fetchall()
	# print ("user",user)
	return render_template("user.html", user=user)

@app.route('/ipn/',methods=['POST'])
def ipn():

	arg = ''
	request.parameter_storage_class = ImmutableOrderedMultiDict
	values = request.form
	for x, y in values.iteritems():
		arg += "&{x}={y}".format(x=x,y=y)

	validate_url = 'https://www.sandbox.paypal.com' \
				   '/cgi-bin/webscr?cmd=_notify-validate{arg}' \
				   .format(arg=arg)
	r = requests.get(validate_url)
	if r.text == 'VERIFIED':

		session['paid_subscription'] = True
		db.execute("INSERT INTO houseclean7(name, password, phone, address, email, years, latitude, longitude, description, hourly_rate, numcleaners, studio, one_bed, two_bed, three_bed, deep_clean, image, broom, mop, vacuum, disinfectant, soap_scum, tooth_brush, scrub_pads, sponges, scraper, paper_towels, paid_subscription) VALUES (:name, :password, :phone, :address, :email, :years, :latitude, :longitude, :description, :hourly_rate, :numcleaners, :studio, :one_bed, :two_bed, :three_bed, :deep_clean, :image, :broom, :mop, :vacuum, :disinfectant, :soap_scum, :tooth_brush, :scrub_pads, :sponges, :scraper, :paper_towels, :paid_subscription)", { "name":session['name'], "password":session['password'], "phone":session['phone'], "address":session['address'], "email":session['email'], "years":session['years'], "latitude":session['latitude'], "longitude":session['longitude'], "description":session['description'], "hourly_rate":session['hourly_rate'], "numcleaners":session['numcleaners'], "studio":session['studio'], "one_bed":session['one_bed'],"two_bed":session['two_bed'],"three_bed":session['three_bed'],"deep_clean":session['deep_clean'],"image":session['image'], "broom":session['broom'], "mop":session['mop'], "vacuum":session['vacuum'], "disinfectant":session['disinfectant'], "soap_scum":session['soap_scum'], "tooth_brush":session['tooth_brush'], "scrub_pads":session['scrub_pads'], "sponges":session['sponges'], "scraper":session['scraper'], "paper_towels":session['paper_towels'], "paid_subscription":session['paid_subscription']})
		db.commit()
		return redirect(url_for("index"))
	else:
		return "Failure"

@app.route('/success/')
def success():
	if session.get("check_houseclean") is True:
		print("check_houseclean=True / cancel upload")
		#return "Please delete account before uploading another"
	else:
		print("check_houseclean=False")
	return render_template("success.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():

	image_file = request.files['image']
	session['image']= image_file.read()
	image = image_file.read()
	return redirect(url_for("uploader2"))

@app.route('/uploader2', methods = ['GET', 'POST'])
def uploader2():
	# print ("image",session['image'])
	db.execute("INSERT INTO photos(image) VALUES (:image)", {"image":session['image']})
	db.commit()
	return 'file uploaded successfully'

@app.route("/signup_check", methods = ["POST"])
def signup_check():

	image_file = request.files['image']
	if image_file == "":
		session['image'] = 0
	else:
		session['image'] = image_file.read()
	print ('sessi==', session['image'])
	session['name'] = request.form.get("name")
	password1 = request.form.get("password")
	salt = "6Agz"
	db_password = password1+salt
	h = hashlib.md5(db_password.encode())
	session['password'] = h.hexdigest()
	phone1 = request.form.get("phone1")
	phone2 = request.form.get("phone2")
	phone3 = request.form.get("phone3")
	string1 = str(phone1)
	string2 = str(phone2)
	string3 = str(phone3)
	session['phone'] = string1 + string2 + string3
	if db.execute("SELECT * FROM houseclean7 WHERE phone = :phone", {"phone": session['phone']}).rowcount > 0:
		return "Number already taken, please contact support at 786-873-7526"
	street = request.form.get("street")
	city = request.form.get("city")
	state = request.form.get("state")
	zip_code = request.form.get("zip_code")
	session['email'] = request.form.get("email")
	session['years'] = request.form.get("years")
	session['description'] = request.form.get("description")
	quot = re.sub('"', '-', session['description'])
	regex = re.sub("\s", " ",quot)
	session['description'] = regex

	session['hourly_rate'] = request.form.get("hourly_rate")
	if session['hourly_rate'] == "":
		session['hourly_rate'] = 0

	session['numcleaners'] = request.form.get("numcleaners")
	if session['numcleaners'] == "":
		session['numcleaners'] = 0

	session['studio'] = request.form.get("studio")
	if session['studio'] == "":
		session['studio'] = 0
	session['one_bed'] = request.form.get("one_bed")
	if session['one_bed'] == "":
		session['one_bed'] = 0
	session['two_bed'] = request.form.get("two_bed")
	if session['two_bed'] == "":
		session['two_bed'] = 0
	session['three_bed'] = request.form.get("three_bed")
	if session['three_bed'] == "":
		session['three_bed'] = 0
	session['deep_clean'] = request.form.get("deep_clean")
	if session['deep_clean'] == "":
		session['deep_clean'] = 0
	session['broom'] = request.form.get("broom")
	session['mop'] = request.form.get("mop")
	session['vacuum'] = request.form.get("vacuum")
	session['disinfectant'] = request.form.get("disinfectant")
	session['soap_scum'] = request.form.get("soap_scum")
	session['tooth_brush'] = request.form.get("tooth_brush")
	session['scraper'] = request.form.get("scraper")
	session['sponges'] = request.form.get("sponges")
	session['scrub_pads'] = request.form.get("scrub_pads")
	session['paper_towels'] = request.form.get("paper_towels")

	if session['broom'] == "on":
		session['broom'] = True
	else:
		session['broom'] = False

	if session['mop'] == "on":
		session['mop'] = True
	else:
		session['mop'] = False

	if session['vacuum'] == "on":
		session['vacuum'] = True
	else:
		session['vacuum'] = False

	if session['disinfectant'] == "on":
		session['disinfectant'] = True
	else:
		session['disinfectant'] = False

	if session['soap_scum'] == "on":
		session['soap_scum'] = True
	else:
		session['soap_scum'] = False

	if session['tooth_brush'] == "on":
		session['tooth_brush'] = True
	else:
		session['tooth_brush'] = False

	if session['scraper'] == "on":
		session['scraper'] = True
	else:
		session['scraper'] = False

	if session['sponges'] == "on":
		session['sponges'] = True
	else:
		session['sponges'] = False

	if session['scrub_pads'] == "on":
		session['scrub_pads'] = True
	else:
		session['scrub_pads'] = False

	if session['paper_towels'] == "on":
		session['paper_towels'] = True
	else:
		session['paper_towels'] = False

	session['address'] = street+", "+city+", "+state+", "+zip_code
	params = {
		'address': session['address'],
		'key': 'AIzaSyD9fytSdXXr6kVZdXLddFJyF9HT4JTt-qM',
	}
	res = requests.get(GOOGLE_MAPS_API_URL, params=params)
	response = res.json()

	latlng=response['results'][0]['geometry']['location']
	session['latitude'] = latlng['lat']
	session['longitude'] = latlng['lng']

	if session.get("check_houseclean") is True:
		print("check_houseclean=True / cancel upload")
		#return "Please delete account before uploading another"
	else:
		print("check_houseclean=False")

	db.execute("INSERT INTO houseclean7(name, password, phone, address, email, years, latitude, longitude, description, hourly_rate, numcleaners, studio, one_bed, two_bed, three_bed, deep_clean, image, broom, mop, vacuum, disinfectant, soap_scum, tooth_brush, scrub_pads, sponges, scraper, paper_towels) VALUES (:name, :password, :phone, :address, :email, :years, :latitude, :longitude, :description, :hourly_rate, :numcleaners, :studio, :one_bed, :two_bed, :three_bed, :deep_clean, :image, :broom, :mop, :vacuum, :disinfectant, :soap_scum, :tooth_brush, :scrub_pads, :sponges, :scraper, :paper_towels )", { "name":session['name'], "password":session['password'], "phone":session['phone'], "address":session['address'], "email":session['email'], "years":session['years'], "latitude":session['latitude'], "longitude":session['longitude'], "description":session['description'], "hourly_rate":session['hourly_rate'], "numcleaners":session['numcleaners'], "studio":session['studio'], "one_bed":session['one_bed'],"two_bed":session['two_bed'],"three_bed":session['three_bed'],"deep_clean":session['deep_clean'],"image":session['image'], "broom":session['broom'], "mop":session['mop'], "vacuum":session['vacuum'], "disinfectant":session['disinfectant'], "soap_scum":session['soap_scum'], "tooth_brush":session['tooth_brush'], "scrub_pads":session['scrub_pads'], "sponges":session['sponges'], "scraper":session['scraper'], "paper_towels":session['paper_towels']})
	db.commit()
	session["check_houseclean"] = True
	print("check_houseclean=True")
	# msg = Message('Hello From House Cleaning Miami', sender = 'housecleanmiami@gmail.com', recipients = [email])
	# msg.body = 'Hello Testing'
	# mail.send(msg)
	# return redirect(url_for("success"))
	return redirect(url_for("index"))
	# '<div class="col-md-2 ">'+
			# '<p id = "column-title" >Photo</p>'+
			# '<div>'+'<img src='+houseclean_list[i]['image']+' alt="image" width="64" height="64"" />'+'</div>'+
			# '</div>'+
