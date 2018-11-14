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

conn = sqlite3.connect('database.db')
cur = conn.cursor()

@app.route('/')
def index():
	return 'Index Page'

@app.route('/hello')
def hello():
	return 'Hello, World'

@app.route('/user')
def viewUser():
	if ('username' in session):
		return "Hello %s" % (session['username'])
	else:
		return 'Please sign in.'

@app.route('/user/<USER>')
def userPage(USER):
	return "User: %s" % (USER)

@app.route('/html')
def html():
	return render_template('test.html', name='Sean')

@app.route('/testlogin', methods=["POST", "GET"])
def testlogin():
	if (request.method=="POST"):
		session['username'] = request.form['username']
		return redirect('/user')
	else:
		return render_template("form.html")
	
@app.route('/makeuser', methods=["POST", "GET"])
def makeuser():
	if (request.method=="POST"):
		userinfo = [request.form['username'], sha256_crypt.hash(request.form['password']), request.form['fact']]
		cur.execute("INSERT INTO users VALUES (?,?,?)", (userinfo))
	else:
		return render_template("make.html")
	
conn.commit()
conn.close()
