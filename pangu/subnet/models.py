# -*- coding: utf-8 -*
from datetime import datetime
from pangu import db

class Subnet(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=True)
    net_type = db.Column(db.Boolean, default=True) # True: private net; False: public net
    gateway = db.Column(db.String(20))
    netmask = db.Column(db.String(20))
    network_addr = db.Column(db.String(20))
    begin_addr = db.Column(db.String(20))
    end_addr = db.Column(db.String(20))
    broadcast_addr = db.Column(db.String(20))
    valid_addr = db.Column(db.Integer)
    used_addr = db.Column(db.Integer)
    notes = db.Column(db.String(200))
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Ip(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=True)
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    subnet_id = db.Column(db.Integer)
    device_id = db.Column(db.Integer, default=0)

class Vlan(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(20), index=True, nullable=False)
    notes = db.Column(db.String(200))
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    subnet_id = db.Column(db.Integer)