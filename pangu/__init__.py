# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.principal import Principal, PermissionDenied, identity_changed, identity_loaded, Identity

app = Flask(__name__)
app.config.from_object('pangu.config')
db = SQLAlchemy(app)
principal = Principal(app)

@app.route('/', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if request.form['username'] == 'admin' and request.form['password'] == 'admin':
			return redirect(url_for('home'))
		else:
			flash(u'无效的用户名或者密码!')	
	return render_template('login.html')

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/server')
def server():
    return render_template('server/list.html')

# register modules
from pangu.manufacture.views import mod as manufactureModule 
app.register_blueprint(manufactureModule, url_prefix='/manufacture')

from pangu.subnet.views import mod as subnetModule
app.register_blueprint(subnetModule, url_prefix='/subnet')

from pangu.datacenter.views import mod as datacenterModule
app.register_blueprint(datacenterModule, url_prefix='/datacenter')

from pangu.account.views import mod as accountModule 
app.register_blueprint(accountModule, url_prefix='/account')