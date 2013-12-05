# -*- coding: utf-8 -*
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import Required, EqualTo, Email

class LocationEditForm(Form):
    short_name = TextField(u'简称')
    full_name = TextField(u'全称')
    ct_bandwidth = TextField(u'电信出口带宽(Mb)')
    cu_bandwidth = TextField(u'联通出口带宽(Mb)')
    other_bandwidth = TextField(u'其他出口带宽(Mb)')
    notes = TextAreaField(u'备注')
    manufacture_id = SelectField(u'关联供应商', coerce=int)

class LocationDetailForm(Form):
    id = TextField(u'#')
    short_name = TextField(u'简称')
    full_name = TextField(u'全称')
    ct_bandwidth = TextField(u'电信出口带宽(Mb)')
    cu_bandwidth = TextField(u'联通出口带宽(Mb)')
    other_bandwidth = TextField(u'其他出口带宽(Mb)')
    notes = TextAreaField(u'备注')
    manufacture_id = SelectField(u'关联供应商', coerce=int)
    update_user = TextField(u'更新用户')
    update_time = TextField(u'更新时间')

class AreaEditForm(Form):
    name = TextField(u'名称')
    notes = TextAreaField(u'备注')
    location_id = SelectField(u'关联机房', coerce=int)

class AreaDetailForm(Form):
    id = TextField(u'#')
    name = TextField(u'名称')
    notes = TextAreaField(u'备注')
    location_id = SelectField(u'关联机房', coerce=int)
    update_user = TextField(u'更新用户')
    update_time = TextField(u'更新时间')

class RackEditForm(Form):
    name = TextField(u'名称')
    units = TextField(u'空间容量(u)')
    capacity = TextField(u'设备总量')
    notes = TextAreaField(u'备注')
    location_id = SelectField(u'关联机房', coerce=int)
    area_id = SelectField(u'关联区域', coerce=int)

class RackDetailForm(Form):
    id = TextField(u'#')
    units = TextField(u'空间容量(u)')
    capacity = TextField(u'设备总量')
    notes = TextAreaField(u'备注')
    location_id = SelectField(u'关联机房', coerce=int)
    area_id = SelectField(u'关联区域', coerce=int)
    update_user = TextField(u'更新用户')
    update_time = TextField(u'更新时间')