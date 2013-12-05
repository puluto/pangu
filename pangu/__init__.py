# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('pangu.config')
db = SQLAlchemy(app)

@app.route('/')
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