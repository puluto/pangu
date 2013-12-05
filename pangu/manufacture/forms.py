# -*- coding: utf-8 -*
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import Required, EqualTo, Email

class EditForm(Form):
    short_name = TextField(u'简称')
    full_name = TextField(u'全称')
    sites = TextField(u'官方网站')
    producer = BooleanField(u'生产商')
    software = BooleanField(u'软件商')
    supplier = BooleanField(u'供应商')
    notes = TextAreaField(u'备注')

class DetailForm(Form):
    id = TextField(u'#')
    short_name = TextField(u'简称')
    full_name = TextField(u'全称')
    sites = TextField(u'官方网站')
    producer = BooleanField(u'生产商')
    software = BooleanField(u'软件商')
    supplier = BooleanField(u'供应商')
    notes = TextAreaField(u'备注')
    update_user = TextField(u'更新用户')
    update_time = TextField(u'更新时间')
