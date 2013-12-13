# -*- coding: utf-8 -*-
from flask.ext.principal import Permission, RoleNeed, ActionNeed

# 组角色权限
normal_role_permission = Permission(RoleNeed('normalGroup')) 		# 普通运维用户(监控, 运营, 库管)
base_role_permission = Permission(RoleNeed('baseGroup'))			# 基础运维部署组
deploy_role_permission = Permission(RoleNeed('deployGroup'))		# 应用运维部署组
admin_role_permission = Permission(RoleNeed('adminGroup'))			# 运维管理员组
network_role_permission = Permission(RoleNeed('networkGroup'))		# 运维网络组
storage_role_permission = Permission(RoleNeed('storageGroup'))		# 运维存储组
capture_role_permission = Permission(RoleNeed('captureGroup'))		# 运维采集组
database_role_permission = Permission(RoleNeed('databaseGroup'))	# 运维数据库组

# 执行权限
detail_action_permission = Permission(ActionNeed('detailAction'))
edit_action_permission = Permission(ActionNeed('editAction'))
delete_action_permission = Permission(ActionNeed('deleteAction'))