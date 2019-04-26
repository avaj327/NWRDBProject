#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 00:06:53 2018
@author: Tyler Johnson and Sean Pergola
"""

from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3
from passlib.hash import sha256_crypt
from clubs import clubs
#TODO https://stackoverflow.com/questions/21498694/flask-get-current-route/21498747
app = Flask(__name__)

templates = {
	"login": "DataBaseLogin1.html",
	"makeuser": "makeuser.html",
	"dataEntry": "index.htm",
	"clubList": "DatabaseClubList1.html",
	"clubListNoUser": "Clublist2.html",
	"user": "UserPageDatabase.html",
	"404": "errorpage404.html",
	"admin": "adminPage.html",
}

pointer = "»"

app.secret_key = "53Da__de39^^w32$5)*8"

userTableFields = """ (
	name varchar(255) NOT NULL PRIMARY KEY,
	hours integer NOT NULL,
	approved integer NOT NULL
	); """

def fixName (clubName):
	for char in clubName:
		if char == '-':
			char = '〰'
			continue
		if char == '〰':
			char = '-'

@app.route('/')
def index():
	return 'Index Page'

@app.route('/hello')
def hello():
	return 'Hello, World'

@app.route('/dataentry', methods=["POST", "GET"])
def dataEntry():
	if (request.method=="POST"):
		user = session['user']
		conn = sqlite3.connect('database.db')
		cur = conn.cursor()
		entry = [session['user'][0], request.form['club'], request.form['activity'], int(request.form['hours']), int(request.form['approved'])]
		cur.execute("INSERT INTO userEntries VALUES(?,?,?,?,?)", entry)
		conn.commit()
		conn.close()
		return "Sent."
	elif ('user' in session):
		user = session['user']
		username = user[0]
		return render_template(templates["dataEntry"], username=username)
	else:
		return redirect("/login")

@app.route('/entrylist')
def viewEntries():
	conn = sqlite3.connect('database.db')
	cur = conn.cursor()
	users = cur.execute("SELECT * FROM userEntries")

	names=[]
	club=[]
	activity=[]
	hours=[]
	approved=[]
	for row in users:
		names.append(row[0])
		club.append(row[1])
		activity.append(row[2])
		hours.append(row[3])
		approved.append(row[4])

	return render_template('entrylist.html', names=names, clubs=club, activities=activity, hours=hours, approved=approved)



@app.route('/clubs', methods=["POST", "GET"])
def clublist():
	if (request.method=="POST"):
		pass#TODO: On POST, use URL paramater to add club to membership list, create SQL table with the address username/club, and refresh page
	else:
		try:
			username = session['user'][0]
			return render_template(templates["clubList"], clublist=clubs.getAll(), username=username,adminlevel=session['user'][2])
		except KeyError:
			return render_template(templates["clubListNoUser"], clublist=clubs.getAll())


@app.route('/user', methods=["POST","GET"])
def viewUser():
	if ('user' in session):
		user = session['user']
		username = user[0] #SEAN ES MUY STUPIDren Club DatabaO
		adminLevel = user[2]
		rawMemberships = user[3].split(",")
		rawAdvisories = user[4].split(",")
		entries = session['entries']

		print (rawMemberships)
		print(rawAdvisories)

		memberships_ = []
		advisories_ = []

		memberships = []
		advisories = []

		membershipClubs = []

		if rawMemberships != ['[]']:
			#strip unnecessary characters for memberships
			for each in rawMemberships:
				i = 0
				length = len(each)
				while i < length:
					if each[i] == " ":
						each = each[:i] + each[i+1:]
					if each[i] == "[":
						each = each[:i] + each[i+1:]
					if each[i] == "]":
						each = each[:i] + each[i+1:]
					if each[i] == "'":
						each = each[:i] + each[i+1:]
					i += 1
					length = len(each)
				each = each[:len(each)]
				memberships_.append(each)

			#STUPID JANK FIX FOR END OF ARRAY ']'
			last = memberships_[len(memberships_)-1]
			lastLen = len(last)-1
			if last[lastLen] == "]":
				last = last[:lastLen]

			memberships_.pop(len(rawMemberships)-1)
			memberships_.append(last)

			last = rawMemberships[len(rawMemberships)-1]
			lastLen = len(last)-1

			#replace '_' with spaces for memberships
			for each in memberships_:
				for i in range(len(each)-1):
					if i < len(each):
						if each[i] == "_":
							each = each[:i] + " " + each[i+1:]
				each = each[:len(each)]
				memberships.append(each)
		else:
			memberships.append("None")

		if rawAdvisories != ['[]']:
			#strip unnecessary characters for advisories
			for each in rawAdvisories:
				i = 0
				length = len(each)-1
				while i <= length:
					if each[i] == " ":
						each = each[:i] + each[i+1:]
					if each[i] == "[":
						each = each[:i] + each[i+1:]
					if each[i] == "]":
						each = each[:i] + each[i+1:]
					if each[i] == "'":
						each = each[:i] + each[i+1:]
					i += 1
					length = len(each)-1
				each = each[:len(each)]
				advisories_.append(each)

			#replace '_' with spaces for advisories
			for each in advisories_:
				for i in range(len(each)-1):
					if i < len(each):
						if each[i] == "_":
							each = each[:i] + " " + each[i+1:]
				each = each[:len(each)]
				advisories.append(each)

		#create membership club array from membership string array
		for each in memberships:
			club = clubs(each)
			for entry in entries:
				if club.name == entry[1]:
					club.addEntry(entry)

			membershipClubs.append(club)

		return render_template(templates["user"], username=username,adminlevel=adminLevel,memberships=membershipClubs,advisories=advisories)
	else:
		return redirect('/login')

@app.route('/admin')
def viewAdmin():
	if 'user' in session:
		user = session['user']
		if user[2] != 0:
			return render_template(templates['admin'],adminlevel=session['user'][2],username=session['user'][0])
		else:
			return redirect('/user')
	else:
		return redirect('/login')

@app.route('/html')
def html():
	return render_template('test.html', name='Sean')

@app.route('/login', methods=["POST", "GET"])
def login():
	if (request.method=="POST"):
		conn = sqlite3.connect('database.db')
		cur = conn.cursor()
		username = request.form['username']
		password = request.form['password']
		user = None
		for row in cur.execute("SELECT * FROM users"):
			if row[0] == username:
				user = row

		if user == None:
			return render_template(templates["login"], incorrect=True)
		else:
			entries = []
			for i,row in enumerate(cur.execute("SELECT * FROM userEntries")):
				if row[0] == username:
					entries.append(row)

		if (sha256_crypt.verify(password, user[1]) == True):
			session['user'] = user
			session['entries'] = entries
		else:
			return render_template(templates["login"], incorrect=True)

		return redirect('/user')
	else:
		return render_template(templates["login"], incorrect=False)

@app.route('/userlist')
def userlist():
	conn = sqlite3.connect('database.db')
	cur = conn.cursor()
	users = cur.execute("SELECT * FROM users")

	names=[]
	passwords=[]
	levels=[]
	memberships=[]
	advisories=[]
	for row in users:
		names.append(row[0])
		passwords.append(row[1])
		levels.append(row[2])
		memberships.append(row[3])
		advisories.append(row[4])

	return render_template('userlist.html', names=names, passwords=passwords, levels=levels, memberships=memberships, advisories=advisories)

@app.route('/makeuser', methods=["POST", "GET"])
def makeuser():
	if (request.method=="POST"):
		conn = sqlite3.connect('database.db')
		cur = conn.cursor()
		userinfo = [request.form['username'], sha256_crypt.hash(request.form['password']), int(request.form['adminLevel']), str(request.form.getlist('memberships')), str(request.form.getlist('advisories'))]
		cur.execute("INSERT INTO users VALUES (?,?,?,?,?)", userinfo)
		conn.commit()
		conn.close()
		return "Sent."
	else:
		return render_template(templates["makeuser"])

@app.errorhandler(404)
def fourohfour(e):
	test = request.path
	for tempurl in app.url_map.iter_rules():
		if str.lower(test) == str.lower(str(tempurl)):
			return redirect(str(tempurl)) #TODO: Fix 404 for /USER

	return render_template(templates["404"], url=str(test))

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/login')
