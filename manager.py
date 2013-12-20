# -*- coding: utf-8 -*-
from flask.ext.script import Manager, Server, prompt_bool
from datetime import datetime
from pangu import app, db
from pangu.manufacture.models import Manufacture 
from pangu.subnet.models import Subnet
from pangu.account.models import User, Resource

manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0', use_debugger=True))

@manager.command
def create_tables():
    db.create_all()

@manager.command
def initial_tables():
    db.session.add_all([
        Manufacture(short_name=u'DELL', full_name=u'戴尔(中国)计算机有限公司', sites=u'http://www.dell.com.cn', \
            producer=True, software=False, supplier=True, notes=u'详细'),
        Manufacture(short_name=u'IBM', full_name=u'国际商用(中国)计算机有限公司', sites=u'http://www.ibm.com.cn', \
            producer=True, software=False, supplier=True, notes=u'详细'),
        Manufacture(short_name=u'infortrend', full_name=u'普安科技有限公司', \
            sites=u'http://www.infortrend.com/tw', producer=True, software=False, supplier=False, notes=u'详细'),
        Manufacture(short_name=u'promise', full_name=u'乔鼎资讯股份有限公司', sites=u'http://www.promise.com', \
            producer=True, software=False, supplier=False, notes=u'详细'),
        Manufacture(short_name=u'Supermicro', full_name=u'超微计算机有限公司', sites=u'http://www.supermicro.com.tw', \
            producer=True, software=False, supplier=False, notes=u'详细'),
        Manufacture(short_name=u'无锡电信', full_name=u'中国电信无锡电信分公司', sites=u'http://js.189.cn/bussiness/page/new/index.html', \
            producer=False, software=False, supplier=True, notes=u'详细')])
    
    db.session.add_all([
        User(name=u'系统管理员', code_name=u'admin', password=u'password', \
            mail='admin@local', mobile='13900000000', leader=False),
        User(name=u'普通登录用户', code_name=u'guest', password=u'guest', \
            mail='guest@local', mobile='13800000000', leader=False)])

    db.session.commit()

@manager.command
def drop_tables():
    if prompt_bool("你确认要删除所有数据?删除执行后数据不可恢复!"):
        db.drop_all()

if __name__ == '__main__':
    manager.run()
