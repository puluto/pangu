# -*- coding: utf-8 -*
from datetime import datetime
from pangu import db

class Manufacture(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True) 
    short_name = db.Column(db.String(20), index=True, unique=True, nullable=False)
    full_name = db.Column(db.String(50), unique=True, nullable=False) 
    sites = db.Column(db.String(50))
    producer = db.Column(db.Boolean, default=False)
    software = db.Column(db.Boolean, default=False)
    supplier = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text(500))
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<User %r>' % (self.short_name)
