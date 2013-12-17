# -*- coding: utf-8 -*
from flask import Blueprint, render_template, flash, redirect, url_for, session, request, g, jsonify
from pangu import db, app
from pangu.account.forms import MenuEditForm, MenuDetailForm
from pangu.account.models import Menu, User, Group, Permission

mod = Blueprint('account', __name__)

@mod.route('/menu/json/select_list/')
def menu_selectlist():
	'''
		Json方法, 获取2级菜单select选项
	'''
	menus = Menu.query.filter(Menu.level_1_id==request.args.get('choice', type=int), Menu.level_2_id==0)
	result	= [{'id': i.id, 'name': i.name} for i in menus]
	return jsonify(json=result)

@mod.route('/menu/')
def menu_list():
	menus = Menu.query.order_by(Menu.id).all()
	parent = [ i.name for i in Menu.query.order_by(Menu.id)]
	return render_template('account/menu_list.html', menus=menus, parent=parent)

@mod.route('/menu/add/', methods=['GET', 'POST'])
def menu_add():
	form = MenuEditForm(request.form)
	form.level_1_id.choices = [(i.id, i.name) for i in Menu.query.filter(Menu.level_1_id==0).all()]
	form.level_1_id.choices.insert(0, (0, u'- 设置为一级菜单 -'))
	form.level_2_id.choices = [(i.id, i.name) \
		for i in Menu.query.filter(Menu.level_1_id!=0, Menu.level_2_id==0).all()]
	form.level_2_id.choices.insert(0, (0, u'- 设置为二级菜单 -'))
	if form.validate_on_submit():
		menu = Menu()
		form.populate_obj(menu)
		db.session.add(menu)
		db.session.commit()
		return redirect(url_for("account.menu_list"))
	return render_template('account/menu_edit.html', form=form)

@mod.route('/menu/detail/<int:id>')
def menu_detail(id):
    menu = Menu.query.filter(Menu.id==id).first()
    form = MenuDetailForm(request.form, menu)
    form.level_1_id.choices = [(i.id, i.name) for i in Menu.query.filter(Menu.level_1_id==0).all()]
    form.level_1_id.choices.insert(0, (0, u'- 设置为一级菜单 -'))
    form.level_2_id.choices = [(i.id, i.name) \
    	for i in Menu.query.filter(Menu.level_1_id!=0, Menu.level_2_id==0).all()]
    form.level_2_id.choices.insert(0, (0, u'- 设置为二级菜单 -'))
    return render_template('account/menu_detail.html', form=form)

@mod.route('/menu/edit/<int:id>', methods=['GET', 'POST'])
def menu_edit(id):
	menu = Menu.query.filter(Menu.id==id).first()
	form = MenuEditForm(request.form, menu)
	form.level_1_id.choices = [(i.id, i.name) for i in Menu.query.filter(Menu.level_1_id==0).all()]
	form.level_1_id.choices.insert(0, (0, u'- 设置为一级菜单 -'))
	form.level_2_id.choices = [(i.id, i.name) \
		for i in Menu.query.filter(Menu.level_1_id!=0, Menu.level_2_id==0).all()]
	form.level_2_id.choices.insert(0, (0, u'- 设置为二级菜单 -'))
	if form.validate_on_submit():
		form.populate_obj(menu)
		db.session.commit()
		return redirect(url_for("account.menu_list"))
	return render_template('account/menu_edit.html', form=form)

@mod.route('/menu/delete/<int:id>')
def menu_delete(id):
	menu = Menu.query.filter(Menu.id==id).first()
	db.session.delete(menu)
	db.session.commit()
	return redirect(url_for("account.menu_list"))