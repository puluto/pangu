# -*- coding: utf-8 -*
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, SelectMultipleField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import Required, EqualTo, Email

from pangu.account.models import User  

class LoginForm(Form):
    username = TextField(u'用户名', [Required()])
    password = PasswordField(u'用户密码', [Required()])
    remember_me = BooleanField(u'记住我', default=False)

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            flash(u'无效用户!')

        if user.password != self.password.data:
            flash(u'无效密码!')

    def get_user(self):
        return User.query.filter(User.name==self.username.data).first()