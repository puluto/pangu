# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config.from_object('pangu.config')
db = SQLAlchemy(app)

# 初始化 flask-login
login_manager = LoginManager()
login_manager.init_app(app)

# flask-login 回调函数
@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id==userid).first()

# 注册蓝图模块
from pangu.manufacture.views import mod as manufactureModule 
app.register_blueprint(manufactureModule, url_prefix='/manufacture')

from pangu.subnet.views import mod as subnetModule
app.register_blueprint(subnetModule, url_prefix='/subnet')

from pangu.datacenter.views import mod as datacenterModule
app.register_blueprint(datacenterModule, url_prefix='/datacenter')

from pangu.account.views import mod as accountModule 
app.register_blueprint(accountModule, url_prefix='/account')

# 用户登录验证
from pangu.auth import current_user_navbar
from pangu.account.models import User

@app.route('/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user=User.query.filter(User.code_name==username).first()

        if username is None or user is None:
            flash(u'无效用户名!')
            return redirect(url_for('login'))
        else:
            auth = check_password_hash(user.password, password)

        if not auth: 
            flash(u'无效密码!')
            return redirect(url_for('login'))
        else:
            # 用户信息放入session
            login_user(user)
            
            # navbar放入session
            session['navbar'] = current_user_navbar(current_user.id)
            return redirect(url_for('home'))

    return render_template('index.html')

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    logout_user()
    session.pop('navbar', None)
    return redirect(url_for('login'))

@app.errorhandler(401)
def unauthorized_page(error):
    return render_template('401.html'), 401

# 首页
@app.route('/home')
@login_required
def home():
	return render_template('home.html')