# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.principal import Principal, PermissionDenied, identity_changed, identity_loaded, Identity

app = Flask(__name__)
app.config.from_object('pangu.config')
db = SQLAlchemy(app)
principal = Principal(app)

@app.route('/')
def index():
    return render_template('index.html')

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

#from pangu.account.views import mod as accountModule 
#app.register_blueprint(accountModule, url_prefix='/account')