# -*- coding: utf-8 -*
from flask import Blueprint, render_template, flash, redirect, url_for, session, request, g, jsonify
from sqlalchemy.orm import aliased
from flask.ext.login import login_user, logout_user, current_user, login_required

from pangu import app, db, login_manager
from pangu.account.forms import ResourceEditForm, ResourceDetailForm, UserEditForm, UserDetailForm, \
	TeamEditForm, TeamDetailForm
from pangu.account.models import Resource, User, Team, Permission


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

@mod.route('/team/json/select_list/')
def team_selectlist():
	'''
		Json方法, 获取2级菜单select选项
	'''
	teams = Team.query.filter(Team.id!=1).order_by(Team.id).all()
	result	= [{'id': i.id, 'name': i.name} for i in teams]
	return jsonify(json=result)

def flag_to_html(value, flag, id):
	if value == True:
		html = '<input type="checkbox" name="' + flag + str(id) + '" checked="checked">'
	else:
		html = '<input type="checkbox" name="' + flag + str(id) + '">'

	return html

@mod.route('/permission/json/get_treeview/')
def get_treeivew():
	'''
		Json方法, 用于生成树形菜单
	'''
	permissions = db.session.query(Resource, Permission) \
		.outerjoin(Permission, Resource.id == Permission.resource_id) \
		.filter(Permission.team_id==request.args.get('team_id', type=int)).all()

	level_1 = [{'id': item[0].id, 'name': item[0].name, \
				'list': flag_to_html(item[1].list_action, 'list', item[1].id), \
				'detail': flag_to_html(item[1].detail_action, 'detail', item[1].id), \
				'edit': flag_to_html(item[1].update_action, 'edit', item[1].id), \
				'delete': flag_to_html(item[1].delete_action, 'delete', item[1].id)} \
		for item in permissions if item[0].level_1_id == 0 and item[0].level_2_id == 0]

	level_2 = [{'_parent': item[0].level_1_id, 'id': item[0].id, 'name': item[0].name, \
				'list': flag_to_html(item[1].list_action, 'list', item[1].id), \
				'detail': flag_to_html(item[1].detail_action, 'detail', item[1].id), \
				'edit': flag_to_html(item[1].update_action, 'edit', item[1].id), \
				'delete': flag_to_html(item[1].delete_action, 'delete', item[1].id)} \
		for item in permissions if item[0].level_1_id != 0 and item[0].level_2_id == 0]
	
	level_3 = [{'_parent': item[0].level_2_id, 'id': item[0].id, 'name': item[0].name, \
				'list': flag_to_html(item[1].list_action, 'list', item[1].id), \
				'detail': flag_to_html(item[1].detail_action, 'detail', item[1].id), \
				'edit': flag_to_html(item[1].update_action, 'edit', item[1].id), \
				'delete': flag_to_html(item[1].delete_action, 'delete', item[1].id)} \
		for item in permissions if item[0].level_1_id != 0 and item[0].level_2_id != 0]

	result = level_1 + level_2 + level_3
	return jsonify(json=result)

@mod.route('/permission/json/post_treeview/', methods=['POST'])
def post_treeivew():
	'''
		Json方法, 树形菜单提交的数据写入数据库
	'''
	if request.method == 'POST':
  		post_data = request.json['json']
  		for i in post_data:
  			permission = Permission.query.filter(Permission.team_id==i['team_id'], \
  				Permission.resource_id==i['id']).first()
  			permission.list_action = i['list']
  			permission.detail_action = i['detail']
  			permission.update_action = i['edit']
  			permission.delete_action = i['delete']
  			db.session.commit()
    	return jsonify(json=post_data)

@mod.route('/resource/')
def resource_list():
	rs1 = aliased(Resource)
	rs2 = aliased(Resource)
	rs3 = aliased(Resource)
	resources = db.session.query(rs1, rs2, rs3) \
		.outerjoin(rs2, rs1.level_1_id == rs2.id) \
		.outerjoin(rs3, rs1.level_2_id == rs3.id) \
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
	write_permission_table()
	return redirect(url_for("account.resource_list"))

@mod.route('/user/')
def user_list():
	users = db.session.query(User, Team).outerjoin(Team, User.team_id == Team.id).all()
	return render_template('account/user_list.html', users=users)

@mod.route('/user/add/', methods=['GET', 'POST'])
def user_add():
	form = UserEditForm(request.form)
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
	return render_template('account/user_detail.html', form=form)

@mod.route('/user/edit/<int:id>', methods=['GET', 'POST'])
def user_edit(id):
	user = User.query.filter(User.id==id).first()
	form = UserEditForm(request.form, user)
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

def write_permission_table(member_list):
	team = Team.query.order_by(Team.id.desc()).first()
	if team is None:
		id = 1
	else:
		id = team.id

	# 用户权限表初始化
	resources = Resource.query.order_by(Resource.id).all()
	db.session.execute(
		Permission.__table__.insert(),
		[{'team_id': id, 'resource_id': resource.id} for resource in resources]
	)

	# 指定用户所属团队
	users = User.query.filter(User.id.in_(member_list)).all()
	for user in users:
		user.team_id = id
	
	db.session.commit()

@mod.route('/team/')
def team_list():
	teams = db.session.query(Team, User).outerjoin(User, Team.leader_id == User.id).all()
	return render_template('account/team_list.html', teams=teams)

@mod.route('/team/add', methods=['GET', 'POST'])
def team_add():
	form = TeamEditForm(request.form)
	form.leader_id.choices = [(i.id, i.name) for i in User.query.filter(User.leader == True).all()]
	form.leader_id.choices.insert(0, (0, u'- 指定负责人 -'))
	form.member_id.choices = [(i.id, i.name) for i in User.query \
		.filter(User.leader == False, User.id != 1, User.team_id==0).all()]
	#form.member_id.choices.insert(0, (0, u'- 指定团队成员 -'))
	if form.validate_on_submit():
		team = Team()
		form.populate_obj(team)
		db.session.add(team)
		db.session.commit()
		# 合并成员
		member = form.member_id.data
		member.append(form.leader_id.data)
		write_permission_table(member)
		return redirect(url_for("account.team_list"))
	return render_template('account/team_edit.html', form=form)

@mod.route('/team/detail/<int:id>')
def team_detail(id):
	team = Team.query.filter(id==id).first()
	form = TeamDetailForm(request.form, team)
	form.leader_id.choices = [(i.id, i.name) \
		for i in User.query.filter(User.leader==True, User.team_id==id).all()]
	form.member_id.choices = [(i.id, i.name) \
		for i in User.query.filter(User.team_id==id, User.leader==False).all()]
	return render_template('account/team_detail.html', form=form)

@mod.route('/team/edit/<int:id>', methods=['GET', 'POST'])
def team_edit(id):
	team = Team.query.filter(Team.id==id).first()
	form = TeamEditForm(request.form, team)
	form.leader_id.choices = [(i.id, i.name) for i in User.query.filter(User.leader == True).all()]
	form.leader_id.choices.insert(0, (0, u'- 指定负责人 -'))
	form.member_id.choices = [(i.id, i.name) for i in User.query \
		.filter(User.leader == False, User.id != 1, User.team_id==id).all()]
	#form.member_id.choices.insert(0, (0, u'- 指定团队成员 -'))
	if form.validate_on_submit():
		form.populate_obj(team)
		# 合并成员
		member = form.member_id.data
		member.append(form.leader_id.data)
		db.session.commit()
		return redirect(url_for("account.team_list"))
	return render_template('account/team_edit.html', form=form)

@mod.route('/team/delete/<int:id>')
def team_delete(id):
	return render_template('home.html')

@mod.route('/permission/')
def permission_edit():
	return render_template('account/permission_edit.html')