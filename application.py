#export FLASK_APP=application.py
#export DATABASE_URL="postgres://ayjxjjxhgpzlnl:f150cc319da46e38a1fb398ee335d98fa5468668d0d8aa3da415aed475d08f9b@ec2-54-225-227-125.compute-1.amazonaws.com:5432/d9prh5mib7dh2p"
#key: 0S6vFxQgJiRIw2CZbc2Yg
# http://exploreflask.com
#secret: 0kmzCjBS62odOXkfg4EcYnoBND3IM28ANuEFlTlWig
#import datetime
from flask import Flask, render_template, request, session, redirect, url_for# Import the class `Flask` from the `flask` module, written by someone else.
from flask_session import Session
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from pprint import pprint
#import csv
import json #for Python to Javascript
import requests #for JSON
import hashlib



app = Flask(__name__) # Instantiate a new web application called `app`, with `__name__` representing the current file

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session (app)

engine = create_engine("postgres://ayjxjjxhgpzlnl:f150cc319da46e38a1fb398ee335d98fa5468668d0d8aa3da415aed475d08f9b@ec2-54-225-227-125.compute-1.amazonaws.com:5432/d9prh5mib7dh2p")
#talk to datbase wiTh SQL. Object used to manage connections to database.
#Sending data to and from database
db = scoped_session(sessionmaker(bind=engine)) # for individual sessions

houseclean_list=[]
#origin="NY"
#destination="Tokyo"
#flight = db.execute("SELECT * FROM flights WHERE origin = :origin AND destination = :dest",  {"origin": origin, "dest": destination} ).fetchone()
#print("flight",flight)
#db.execute("DELETE FROM flights WHERE origin = :origin", {"origin": origin})


#db.execute("CREATE TABLE houseclean1(id SERIAL PRIMARY KEY, name VARCHAR NOT NULL, password VARCHAR NOT NULL, phone VARCHAR NOT NULL UNIQUE, address VARCHAR NOT NULL, latitude FLOAT NOT NULL, longitude FLOAT NOT NULL, email VARCHAR NOT NULL, years SMALLINT NOT NULL, description VARCHAR NOT NULL, hourly_rate SMALLINT NOT NULL, paid_subscription BOOLEAN, image BYTEA)")
#db.commit()
#print("dbcreated")

@app.route("/", methods = ["GET"]) # A decorator; when the user goes to the route `/`, exceute the function immediately below
def index():
	housecleanDB = db.execute("SELECT * FROM houseclean1").fetchall()
	print("housecleanDB",housecleanDB)

	for i in housecleanDB:
		#print("housecleansD",i)
		m = memoryview(i.image)
		image = m.hex()
		print("image",image)
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
		 	"image": image,

			}
		# image_binary = read_image(i.image)

		# img = open(i.image, 'rb').read()
		# response = requests.post(URL, data=img)

		#print ("description",i.description)
		print ("years",i.years)
		print ("image",i.image)
		houseclean_list.append(houseclean_data)
	return render_template("index.html", houseclean_list=houseclean_list)

@app.route("/signup", methods = ["POST"]) #way to get sign in from index to sign-up page
def signup():
	return render_template("signup.html")

@app.route("/delete_account/<string:phone>", methods = ["POST"]) #way to get sign in from index to sign-up page
def delete_account(phone):

	db.execute("DELETE FROM houseclean1 WHERE phone = :phone", {"phone": phone})
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

	if db.execute("SELECT * FROM houseclean1 WHERE name = :name AND password = :password", {"name": name, "password": password}).rowcount == 0:
		return "name and password dont match"
	else:
		user = db.execute("SELECT * FROM houseclean1 WHERE name = :name AND password = :password", {"name": name, "password": password}).fetchall()
	print ("user",user)
	return render_template("user.html", user=user)

@app.route("/signup_check", methods = ["POST"])
def signup_check():
	image = request.form.get("image")

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

	if db.execute("SELECT * FROM houseclean1 WHERE phone = :phone", {"phone": phone}).rowcount > 0:
		return "Number already taken, please contact support at 786-873-7526"
	street = request.form.get("street")
	city = request.form.get("city")
	state = request.form.get("state")
	zip_code = request.form.get("zip_code")
	email = request.form.get("email")
	years = request.form.get("years")
	description = request.form.get("description")
	hourly_rate = request.form.get("hourly_rate")



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


	#db.execute("INSERT INTO houseclean1(name, password, phone, address, email, latitude, longitude, years, description, hourly_rate, image) VALUES (:name, :password, :phone, :address, :email, :latitude, :longitude,  :years, :description, :hourly_rate, :image)", {"name":name, "password":password, "phone":phone, "address":address, "email":email, "latitude":latitude, "longitude":longitude,  "years":years, "description":description, "hourly_rate":hourly_rate, "image":image})
	db.commit()
	session["check_houseclean"] = True
	print("check_houseclean=True")
	return redirect(url_for("index"))
