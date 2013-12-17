# -*- coding: utf-8 -*
from datetime import datetime
from pangu import db

class User(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=True, nullable=False)
    code_name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    mail = db.Column(db.String(50), unique=True, nullable=False)
    mobile = db.Column(db.String(50), unique=True, nullable=False) 
    notes = db.Column(db.String(200))
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    group_id = db.Column(db.Integer, default=0)

class Group(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(20), index=True)
    notes = db.Column(db.String(200))
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    permission_id = db.Column(db.Integer,default=0)

class Menu(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(20), index=True, nullable=False)
    code_name = db.Column(db.String(20), index=True, nullable=False)
    url = db.Column(db.String(20))
    level_1_id = db.Column(db.Integer) # 0,表明为1级菜单; 非0,表明为2级菜单; 
    level_2_id = db.Column(db.Integer) # 0,表明为2级菜单; 非0,表明为3级菜单; 
    notes = db.Column(db.String(200))
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Module(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(20), index=True)
    notes = db.Column(db.String(200))
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Permission(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.Integer)
    notes = db.Column(db.String(200))
    list_action = db.Column(db.String(100))   # 添加group_id,以逗号分隔
    add_action = db.Column(db.String(100))    # 添加group_id,以逗号分隔
    update_action = db.Column(db.String(100)) # 添加group_id,以逗号分隔
    delete_action = db.Column(db.String(100)) # 添加group_id,以逗号分隔
    update_user = db.Column(db.String(20), default='admin')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    module_id = db.Column(db.Integer)