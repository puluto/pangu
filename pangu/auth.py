# -*- coding: utf-8 -*-
from pangu import db
from pangu.account.models import User, Team, Resource, Permission 

# user navbar item
def current_user_navbar(id):
	user = User.query.filter(User.id==id).first()
	resources = db.session.query(Resource, Permission) \
		.outerjoin(Permission, Resource.id==Permission.resource_id) \
		.filter(Permission.team_id==user.team_id, Permission.list_action==True) \
		.order_by(Resource.code_name).all()

	navbar = [{'id': resource[0].id, 'name': resource[0].name, 'code': resource[0].code_name, \
		'url': resource[0].url, 'level_1': resource[0].level_1_id, 'level_2': resource[0].level_1_id} \
		for resource in resources]
	
	return navbar

# user route access control
def current_user_permisson(id):
	return True