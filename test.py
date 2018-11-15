#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 00:06:53 2018

@author: Tyler Johnson
"""

from flask import Flask, request, render_template, session, redirect
import sqlite3
from passlib.hash import sha256_crypt
app = Flask(__name__)

app.secret_key = "53Da__de39^^w32$5)*8"

@app.route('/')
def index():
	return 'Index Page'

@app.route('/hello')
def hello():
	return 'Hello, World'

@app.route('/user')
def viewUser():
	if ('username' in session):
		user = session['user']
		username = user[0]
		password = user[1]
		fact = user[2]
		
		return render_template('user.html', username=username,password=password,fact=fact)
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
		user = None
		for row in cur.execute("SELECT * FROM users"):
			if row[0] == username:
				user = row
				
		if user == None:
			return 'Invalid Username'
			
		if password == user[1]:
			session['user'] = user
		else:
			return 'Invalid Password'
			
		return redirect('/user')
	else:
		return render_template("form.html")
	

@app.route('/makeuser', methods=["POST", "GET"])
def makeuser():
	if (request.method=="POST"):
		conn = sqlite3.connect('database.db')
		cur = conn.cursor()
		userinfo = [request.form['username'], sha256_crypt.hash(request.form['password']), request.form['fact']]
		cur.execute("INSERT INTO users VALUES (?,?,?)", (userinfo))
		conn.commit()
		conn.close()
		return 'Sent.'
	else:
		return render_template("makeuser.html")
