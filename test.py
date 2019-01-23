#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 00:06:53 2018
@author: Tyler Johnson and Sean Pergola
"""

from flask import Flask, request, render_template, session, redirect
import sqlite3
from passlib.hash import sha256_crypt
from clubs import clubs
app = Flask(__name__)

templates = {
	"login": "DataBaseLogin1.html",
	"makeuser": "makeuser.html",
	"dataEntry": "index.htm",
	"clubList": "DatabaseClubList1.html",
	"user": "UserPageDatabase.html"
}

app.secret_key = "53Da__de39^^w32$5)*8"

@app.route('/')
def index():
	return 'Index Page'

@app.route('/hello')
def hello():
	return 'Hello, World'

@app.route('/dataEntry/', methods=["POST", "GET"])
def viewDataEntry():
    if (request.method=="POST"):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        #cur.execute()
        conn.commit()
        conn.close()
        return "Sent."
    elif ('user' in session):
        user = session['user']
        username = user[0]
        return render_template(templates["dataEntry"], username=username)
    else:
        return redirect("/login")

@app.route('/clublist', methods=["POST","GET"])
def clublist():
	if not 'user' in session:
		redirect('/login')
	if (request.method=="POST"):
		pass
	
	return render_template(templates["clubList"], clublist=clubs.getAll())

def fixString(orig, array, new):
	for item in array:
		for i, char in enumerate(orig):
			if char == item:
				orig = orig[:i] + new + orig[i+1:]
	return orig

@app.route('/user/')
def viewUser():
	if ('user' in session):
		user = session['user']
		username = user[0]	
		adminLevel = user[2]
		
		#temporary arrays that contain bad characters
		rawMemberships = user[3].split(",")
		rawAdvisories = user[4].split(",")
		
		badChars = [" ", "[", "]", "'", "'"]

		#temporary arrays for parsing bad characters
		memberships_ = []
		advisories_ = []
		memberships = []
		advisories = []
		
		#arrays filled with "clubs" objects
		membershipClubs = []
		
		try:
			#strip unnecessary characters for memberships
			for each in rawMemberships:
				each = fixString(each, badChars, "")
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
				each = fixString(each, ["_"], " ")
				memberships.append(each)
		except: #in the case of errors parsing club names, fall back to saying no clubs
			memberships.append("None")

		try:
			#strip unnecessary characters for advisories
			for each in rawAdvisories:
				each = fixString(each, badChars, "")
				advisories_.append(each)
			
			#STUPID JANK FIX FOR END OF ARRAY ']'
			last = advisories_[len(advisories_)-1]
			lastLen = len(last)-1
			if last[lastLen] == "]":
					last = last[:lastLen]
		
			advisories_.pop(len(rawAdvisories)-1)
			advisories_.append(last)
				
			last = rawAdvisories[len(rawAdvisories)-1]
			lastLen = len(last)-1
			
			#replace '_' with spaces for advisories
			for each in advisories_: 
				each = fixString(each, ["_"], " ")
				advisories.append(each)
		except: #in the case of errors parsing club names, fall back to saying no advisories
			advisories.append("None")

		#create membership club array from membership string array
		for each in memberships:
			 club = clubs(each)
			 membershipClubs.append(club)
    
		return render_template(templates["user"], username=username,adminLevel=adminLevel,memberships=membershipClubs,advisories=advisories)
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

		if (sha256_crypt.verify(password, user[1]) == True):
			session['user'] = user
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
		userinfo = [request.form['username'], sha256_crypt.hash(request.form['password']), int(request.form['adminLevel']), str(request.form.getlist('memberships')), "none"]
		cur.execute("INSERT INTO users VALUES (?,?,?,?,?)", userinfo)
		conn.commit()
		conn.close()
		return "Sent."
	else:
		return render_template(templates["makeuser"])

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/login')