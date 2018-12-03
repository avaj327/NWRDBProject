
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 00:06:53 2018
@author: Sean Pergola and Tyler Johnson
"""

from flask import Flask, request, render_template, session, redirect
import sqlite3
from passlib.hash import sha256_crypt
app = Flask(__name__)

templates = {
	"login": "nwr form.html",
	"makeuser": "makeuser.html",
	"user": "user.html"
}

app.secret_key = "53Da__de39^^w32$5)*8"

@app.route('/')
def index():
	return 'Index Page'

@app.route('/hello')
def hello():
	return 'Hello, World'

@app.route('/user')
def viewUser():
	if ('user' in session):
		user = session['user']
		username = user[0]
		password = user[1]
		adminLevel = user[2]

		return render_template(templates["user"], username=username,password=password,adminLevel=adminLevel)
	else:
		return 'Please sign in.'
    
@app.route('/mod')
def viewUser():
	if ('user' in session):
		user = session['user']
		username = user[0]
		password = user[1]
		adminLevel = user[2]

		return "ADVISOR!"
	else:
		return 'Please sign in.'
    

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
		adminLevel = request.form["adminLevel"]
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

		if adminLevel == 1:
			return redirect('/mod')
        
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
	for row in users:
		names.append(row[0])
		passwords.append(row[1])
		levels.append(row[2])

	return render_template('userlist.html', names=names, passwords=passwords, levels=levels)

@app.route('/makeuser', methods=["POST", "GET"])
def makeuser():
	if (request.method=="POST"):
		conn = sqlite3.connect('database.db')
		cur = conn.cursor()
		userinfo = [request.form['username'], sha256_crypt.hash(request.form['password']), int(request.form['adminLevel']), "", ""]
		cur.execute("INSERT INTO users VALUES (?,?,?,?,?)", userinfo)
		conn.commit()
		conn.close()
		return 'Sent.'
	else:
		return render_template(templates["makeuser"])