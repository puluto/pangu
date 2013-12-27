# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.config.from_object('pangu.config')
db = SQLAlchemy(app)

# 初始化flask-login
login_manager = LoginManager(app)

# 回调函数
@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id==userid)

# register modules
from pangu.manufacture.views import mod as manufactureModule 
app.register_blueprint(manufactureModule, url_prefix='/manufacture')

from pangu.subnet.views import mod as subnetModule
app.register_blueprint(subnetModule, url_prefix='/subnet')

from pangu.datacenter.views import mod as datacenterModule
app.register_blueprint(datacenterModule, url_prefix='/datacenter')

from pangu.account.views import mod as accountModule 
app.register_blueprint(accountModule, url_prefix='/account')

# 用户登录
from pangu.loginform import LoginForm

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = form.get_user()      # LoginForm方法get_user,获取登录用户对象
        login_user(user)             # 登录用户放入session
        flash('登录成功!')
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/server')
def server():
    return render_template('server/list.html')