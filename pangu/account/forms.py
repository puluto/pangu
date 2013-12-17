# -*- coding: utf-8 -*
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, SelectMultipleField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import Required, EqualTo, Email

class MenuEditForm(Form):
    name = TextField(u'名称', [Required()])
    code_name = TextField(u'英文名称', [Required()])
    url = TextField(u'url')
    notes = TextAreaField(u'备注')
    level_1_id = SelectField(u'关联一级菜单', coerce=int)
    level_2_id = SelectField(u'关联二级菜单', coerce=int)

class MenuDetailForm(Form):
    id = TextField(u'#')
    name = TextField(u'名称', [Required()])
    code_name = TextField(u'英文名称', [Required()])
    url = TextField(u'url')
    notes = TextAreaField(u'备注')
    level_1_id = SelectField(u'关联一级菜单', coerce=int)
    level_2_id = SelectField(u'关联二级菜单', coerce=int)
    update_user = TextField(u'更新用户')
    update_time = TextField(u'更新时间')