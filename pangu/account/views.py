# -*- coding: utf-8 -*
from flask import Blueprint, render_template, flash, redirect, url_for, session, request, g, jsonify
from sqlalchemy.orm import aliased

from pangu import db, app
from pangu.account.forms import ResourceEditForm, ResourceDetailForm, UserEditForm, UserDetailForm, \
	TeamEditForm, TeamDetailForm
from pangu.account.models import Resource, User, Team

mod = Blueprint('account', __name__)

@mod.route('/resource/json/select_list/')
def resource_selectlist():
	'''
		Json方法, 获取2级菜单select选项
	'''
	resources = Resource.query.filter(Resource.level_1_id==request.args.get('choice', type=int), \
			Resource.level_2_id==0)
	result	= [{'id': i.id, 'name': i.name} for i in resources]
	return jsonify(json=result)

@mod.route('/resource/')
def resource_list():
	rs1 = aliased(Resource)
	rs2 = aliased(Resource)
	rs3 = aliased(Resource)
	resources = db.session.query(rs1, rs2, rs3) \
		.outerjoin(rs2, rs1.level_1_id == rs2.id) \
		.outerjoin(rs3, rs1.level_1_id == rs3.id) \
		.all()
	return render_template('account/resource_list.html', resources=resources)

@mod.route('/resource/add/', methods=['GET', 'POST'])
def resource_add():
	form = ResourceEditForm(request.form)
	form.level_1_id.choices = [(i.id, i.name) for i in Resource.query.filter(Resource.level_1_id==0).all()]
	form.level_1_id.choices.insert(0, (0, u'- 设置为一级菜单 -'))
	form.level_2_id.choices = [(i.id, i.name) \
		for i in Resource.query.filter(Resource.level_1_id!=0, Resource.level_2_id==0).all()]
	form.level_2_id.choices.insert(0, (0, u'- 设置为二级菜单 -'))
	if form.validate_on_submit():
		resource = Resource()
		form.populate_obj(resource)
		db.session.add(resource)
		db.session.commit()
		return redirect(url_for("account.resource_list"))
	return render_template('account/resource_edit.html', form=form)

@mod.route('/resource/detail/<int:id>')
def resource_detail(id):
    resource = Resource.query.filter(Resource.id==id).first()
    form = ResourceDetailForm(request.form, resource)
    form.level_1_id.choices = [(i.id, i.name) for i in resource.query.filter(resource.level_1_id==0).all()]
    form.level_1_id.choices.insert(0, (0, u'- 设置为一级菜单 -'))
    form.level_2_id.choices = [(i.id, i.name) \
    	for i in Resource.query.filter(Resource.level_1_id!=0, Resource.level_2_id==0).all()]
    form.level_2_id.choices.insert(0, (0, u'- 设置为二级菜单 -'))
    return render_template('account/resource_detail.html', form=form)

@mod.route('/resource/edit/<int:id>', methods=['GET', 'POST'])
def resource_edit(id):
	resource = Resource.query.filter(Resource.id==id).first()
	form = ResourceEditForm(request.form, resource)
	form.level_1_id.choices = [(i.id, i.name) for i in Resource.query.filter(Resource.level_1_id==0).all()]
	form.level_1_id.choices.insert(0, (0, u'- 设置为一级菜单 -'))
	form.level_2_id.choices = [(i.id, i.name) \
		for i in Resource.query.filter(Resource.level_1_id!=0, Resource.level_2_id==0).all()]
	form.level_2_id.choices.insert(0, (0, u'- 设置为二级菜单 -'))
	if form.validate_on_submit():
		form.populate_obj(resource)
		db.session.commit()
		return redirect(url_for("account.resource_list"))
	return render_template('account/resource_edit.html', form=form)

@mod.route('/resource/delete/<int:id>')
def resource_delete(id):
	resource = Resource.query.filter(Resource.id==id).first()
	db.session.delete(resource)
	db.session.commit()
	return redirect(url_for("account.resource_list"))

@mod.route('/user/json/member_list/')
def user_memberlist():
	'''
		Json方法, 获得团队的人数, 负责人, 成员列表
	'''
	'''
	users = Resource.query.filter(Resource.level_1_id==request.args.get('choice', type=int), \
			Resource.level_2_id==0)
	result	= [{'id': i.id, 'name': i.name} for i in resources]
	return jsonify(json=result)
	'''
	pass

@mod.route('/user/')
def user_list():
	users = db.session.query(User, Team) \
		.outerjoin(Team, User.team_id == Team.id).all()
	return render_template('account/user_list.html', users=users)

@mod.route('/user/add/', methods=['GET', 'POST'])
def user_add():
	form = UserEditForm(request.form)
	form.team_id.choices = [(i.id, i.name) for i in Team.query.all()]
	form.team_id.choices.insert(0, (0, u'- 关联团队 -'))
	if form.validate_on_submit():
		user = User()
		form.populate_obj(user)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("account.user_list"))
	return render_template('account/user_edit.html', form=form)

@mod.route('/user/detail/<int:id>')
def user_detail(id):
	user = User.query.filter(User.id==id).first()
	form = UserDetailForm(request.form, user)
	form.team_id.choices = [(i.id, i.name) for i in Team.query.all()]
	form.team_id.choices.insert(0, (0, u'- 关联用户组 -'))
	return render_template('account/user_detail.html', form=form)

@mod.route('/user/edit/<int:id>', methods=['GET', 'POST'])
def user_edit(id):
	user = User.query.filter(User.id==id).first()
	form = UserEditForm(request.form, user)
	form.team_id.choices = [(i.id, i.name) for i in Team.query.all()]
	form.team_id.choices.insert(0, (0, u'- 关联用户组 -'))
	if form.validate_on_submit():
		form.populate_obj(user)
		db.session.commit()
		return redirect(url_for("account.user_list"))
	return render_template('account/user_edit.html', form=form)

@mod.route('/user/delete/<int:id>')
def user_delete(id):
	user = User.query.filter(User.id==id).first()
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for("account.user_list"))

@mod.route('/team/')
def team_list():
	teams = db.session.query(Team, User) \
		.outerjoin(User, Team.leader_id == User.id).all()
	return render_template('account/team_list.html', teams=teams)

@mod.route('/team/add', methods=['GET', 'POST'])
def team_add():
	form = TeamEditForm(request.form)
	form.leader_id.choices = [(i.id, i.name) for i in User.query.filter(User.leader == True).all()]
	form.leader_id.choices.insert(0, (0, u'- 指定负责人 -'))
	if form.validate_on_submit():
		team = Team()
		form.populate_obj(team)
		db.session.add(team)
		db.session.commit()
		return redirect(url_for("account.team_list"))
	return render_template('account/team_edit.html', form=form)

@mod.route('/team/detail/<int:id>')
def team_detail(id):
	return render_template('home.html')

@mod.route('/team/edit/<int:id>', methods=['GET', 'POST'])
def team_edit(id):
	team = Team.query.filter(Team.id==id).first()
	form = TeamEditForm(request.form, team)
	form.leader_id.choices = [(i.id, i.name) for i in User.query.filter(User.leader == True).all()]
	form.leader_id.choices.insert(0, (0, u'- 指定负责人 -'))
	if form.validate_on_submit():
		form.populate_obj(team)
		db.session.commit()
		return redirect(url_for("account.team_list"))
	return render_template('account/team_edit.html', form=form)

@mod.route('/team/delete/<int:id>')
def team_delete(id):
	return render_template('home.html')