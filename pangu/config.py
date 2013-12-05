# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'pangu.db')
SQLALCHEMY_DATABASE_URI = 'mysql://pangu:pangu@localhost/pangu'
SQLALCHEMY_ECHO = True

CSRF_ENABLED = True
SECRET_KEY = '1b928ffa-4688-11e3-ade9-87e795cd55cc'