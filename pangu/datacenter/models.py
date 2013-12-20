# -*- coding: utf-8 -*
from datetime import datetime
from pangu import db

class Location(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    short_name = db.Column(db.String(20), index=True, unique=True)
    code_name = db.Column(db.String(20), index=True)
    ct_bandwidth = db.Column(db.Integer, default=0)
    cu_bandwidth = db.Column(db.Integer, default=0)
    other_bandwidth = db.Column(db.Integer, default=0)
    notes = db.Column(db.String(200))
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    manufacture_id = db.Column(db.Integer)

class Area(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=True)
    notes = db.Column(db.String(200))
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    location_id = db.Column(db.Integer)

class Rack(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(20), index=True)
    units = db.Column(db.Integer, default=45)
    capacity = db.Column(db.Integer, default=13)
    notes = db.Column(db.String(200))
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    location_id = db.Column(db.Integer)
    area_id = db.Column(db.Integer)
    vlan_id = db.Column(db.String(200))  # 机柜关联多个vlan,使用string类型,如 1,2,3,4,5,6 

class Unit(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(20), index=True)
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    left_dev_id = db.Column(db.Integer, default=0)     # 类似双子星设备左半部
    right_dev_id = db.Column(db.Integer, default=0)    # 类似双子星设备右半部
    all_dev_id = db.Column(db.Integer, default=0)      # 标准机架设备
    rack_id = db.Column(db.Integer)