# -*- coding: utf-8 -*
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, SelectMultipleField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import Required, EqualTo, Email

class ResourceEditForm(Form):
    name = TextField(u'名称', [Required()])
    code_name = TextField(u'英文名称', [Required()])
    url = TextField(u'url')
    notes = TextAreaField(u'备注')
    level_1_id = SelectField(u'关联一级菜单', coerce=int)
    level_2_id = SelectField(u'关联二级菜单', coerce=int)

class ResourceDetailForm(Form):
    id = TextField(u'#')
    name = TextField(u'名称', [Required()])
    code_name = TextField(u'英文名称', [Required()])
    url = TextField(u'url')
    notes = TextAreaField(u'备注')
    level_1_id = SelectField(u'关联一级菜单', coerce=int)
    level_2_id = SelectField(u'关联二级菜单', coerce=int)
    update_user = TextField(u'更新用户')
    update_time = TextField(u'更新时间')

class UserEditForm(Form):
    name = TextField(u'中文姓名', [Required()])
    code_name = TextField(u'中文全拼', [Required()])
    password = TextField(u'密码(hash加密)', [Required()])
    confirm_password = TextField(u'重复密码', [Required()])
    mail = TextField(u'邮件地址')
    mobile = TextField(u'移动电话')
    leader = BooleanField(u'可担任负责人')
    notes = TextAreaField(u'备注')

class UserDetailForm(Form):
    id = TextField(u'#')
    name = TextField(u'中文姓名', [Required()])
    code_name = TextField(u'中文全拼', [Required()])
    mail = TextField(u'邮件地址')
    mobile = TextField(u'移动电话')
    notes = TextAreaField(u'备注')
    update_user = TextField(u'更新用户')
    update_time = TextField(u'更新时间')

class TeamEditForm(Form):
    name = TextField(u'团队名称', [Required()])
    leader_id = SelectField(u'团队负责人', coerce=int)
    member_id = SelectMultipleField(u'团队成员', coerce=int)
    notes = TextAreaField(u'备注')

class TeamDetailForm(Form):
    id = TextField(u'#')
    name = TextField(u'团队名称', [Required()])
    leader_id = SelectField(u'团队负责人', coerce=int)
    member_id = SelectMultipleField(u'团队成员', coerce=int)
    notes = TextAreaField(u'备注')
    update_user = TextField(u'更新用户')
    update_time = TextField(u'更新时间')