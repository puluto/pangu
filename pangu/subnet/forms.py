# -*- coding: utf-8 -*
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import Required, EqualTo, Email

class VlanEditForm(Form):
    name = TextField(u'名称')
    notes = TextAreaField(u'备注')
    subnet_id = SelectField(u'关联子网', coerce=int)

class VlanDetailForm(Form):
    id = TextField(u'#')
    name = TextField(u'名称')
    notes = TextAreaField(u'备注')
    subnet_id = SelectField(u'关联子网', coerce=int)
    update_user = TextField(u'更新用户')
    update_time = TextField(u'更新时间')

class NetAddForm(Form):
	name = TextField(u'子网名称')
	ipaddr_info = TextField(u'地址信息')
	notes = TextAreaField(u'备注')