# -*- coding: utf-8 -*
from datetime import datetime
from pangu import db

class Resource(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(20), index=True, nullable=False)
    code_name = db.Column(db.String(20), index=True, nullable=False)
    url = db.Column(db.String(200))
    level_1_id = db.Column(db.Integer) # 0,表明为1级菜单; 非0,表明为2级菜单; 
    level_2_id = db.Column(db.Integer) # 0,表明为2级菜单; 非0,表明为3级菜单; 
    notes = db.Column(db.String(200))
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Permission(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    list_action = db.Column(db.Boolean, default=False)
    detail_action = db.Column(db.Boolean, default=False)
    update_action = db.Column(db.Boolean, default=False)
    delete_action = db.Column(db.Boolean, default=False)
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    team_id = db.Column(db.Integer, default=0)
    resource_id = db.Column(db.Integer, default=0)

class User(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=True, nullable=False)
    code_name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    mail = db.Column(db.String(50), unique=True, nullable=False)
    mobile = db.Column(db.String(50), unique=True, nullable=False)
    leader = db.Column(db.Boolean, default=False) # 是否为团队负责人
    notes = db.Column(db.String(200))
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    team_id = db.Column(db.Integer, default=0)

class Team(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(20), index=True)
    notes = db.Column(db.String(200))
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    leader_id = db.Column(db.Integer, default=0) # 团队负责人
    resource_id = db.Column(db.Integer, default=0)