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

@app.route('/user/')
def viewUser():
	if ('user' in session):
		user = session['user']
		username = user[0]
		password = user[1]
		adminLevel = user[2]
		rawMemberships = user[3].split(",")
		rawAdvisories = user[4].split(",")

		memberships_ = []
		advisories_ = []

		memberships = []
		advisories = []

		for each in rawMemberships: #strip unnecessary characters
			for i in range(len(each)-1):
				if i < len(each)-1:
					if each[i] == " ":
						each = each[:i] + each[i+1:]
					if each[i] == "[":
						each = each[:i] + each[i+1:]
					if each[i] == "]":
						each = each[:i] + each[i+1:]
					if each[i] == "'":
						each = each[:i] + each[i+1:]
			each = each[:len(each)-1]
			memberships_.append(each)

		for each in memberships_: #replace '_' with spaces
			for i in range(len(each)-1):
				if i < len(each)-1:
					if each[i] == "_":
						each = each[:i] + " " + each[i+1:]
			each = each[:len(each)-1]
			memberships.append(each)

		for each in rawAdvisories: #strip unnecessary characters
			for i in range(len(each)-1):
				if i < len(each)-1:
					if each[i] == " ":
						each = each[:i] + each[i+1:]
					if each[i] == "[":
						each = each[:i] + each[i+1:]
					if each[i] == "]":
						each = each[:i] + each[i+1:]
					if each[i] == "'":
						each = each[:i] + each[i+1:]
			each = each[:len(each)-1]
			advisories_.append(each)

		for each in advisories_: #replace '_' with spaces
			for i in range(len(each)-1):
				if i < len(each)-1:
					if each[i] == "_":
						each = each[:i] + " " + each[i+1:]
			each = each[:len(each)-1]
			advisories.append(each)

		return render_template(templates["user"], username=username,password=password,adminLevel=adminLevel,memberships=memberships,advisories=advisories)
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
		return 'Sent.'
	else:
		return render_template(templates["makeuser"])
