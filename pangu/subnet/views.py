# -*- coding: utf-8 -*
from flask import Blueprint, render_template, flash, redirect, url_for, session, request, g, jsonify
from pangu import db, app
from pangu.subnet.forms import VlanEditForm, VlanDetailForm, NetAddForm
from pangu.subnet.models import Vlan, Subnet, Ip

from netaddr import *

mod = Blueprint('subnet', __name__)

@mod.route('/net/')
def net_list():
	nets = Subnet.query.order_by(Subnet.id)
	return render_template('subnet/net_list.html', nets=nets)

@mod.route('/net/tools')
def tools():
	return render_template('subnet/tools.html')

def write_ip_table(net):
	# insert info of subnet into table
	subnet = Subnet()
	ip = Ip()

	info = IPNetwork(net)
	
	subnet.name = net
	subnet.gateway = info[1]
	subnet.netmask = info.netmask
	subnet.network_addr = info.network
	subnet.begin_addr = info[1]
	subnet.end_addr = info[-2]
	subnet.broadcast_addr = info[-1]
	
	if IPAddress(subnet.network_addr).is_private():
		subnet.net_type = True
	else:
		subnet.net_type = False
	
	subnet.valid_addr = info.size - 2
	subnet.used_addr = 0

	db.session.add(subnet)
	db.session.commit()

	# insert ipaddress of the subnet into table
	subnet_info = Subnet.query.filter_by(name=net).first()
	db.session.execute(
		Ip.__table__.insert(),
		[{'name': info[i], 'subnet_id': subnet_info.id} for i in xrange(1, info.size-1)]
	)
	db.session.commit()

@mod.route('/net/add/', methods=['GET', 'POST'])
def net_add():
	form = NetAddForm()
	if form.validate_on_submit and form.name.data:
		if form.ipaddr_info.data:
			write_ip_table(form.name.data)
			return redirect(url_for('subnet.net_list'))
		else:
			info = IPNetwork(form.name.data)
			form.ipaddr_info.data = str(info[0])+ ',' + str(info[1]) + ',' + str(info[-2])+ ',' + str(info[-1])
			return render_template('subnet/net_add.html', form=form)
	return render_template('subnet/net_add.html', form=form)

@mod.route('/net/detail/<int:id>')
def net_detail(id):
	subnet = Subnet.query.filter_by(id=id).first()
	ip_list = Ip.query.filter_by(subnet_id=subnet.id).all()
	return render_template('subnet/net_detail.html', subnet=subnet, ip_list=ip_list)

@mod.route('/net/delete/<int:id>')
def net_delete(id):
	# 判断子网所属ip是否被使用? 如使用，不能被删除。涉及ip表。
	net = Subnet.query.filter_by(id=id).first()
	db.session.query(Ip).filter(Ip.subnet_id==net.id).delete()
	db.session.delete(net)
	db.session.commit()
	return redirect(url_for('subnet.net_list'))

@mod.route('/vlan/')
def vlan_list():
	vlans = db.session.query(Vlan, Subnet).outerjoin(Subnet, Vlan.subnet_id==Subnet.id).all()
	return render_template('subnet/vlan_list.html', vlans=vlans)

@mod.route('/vlan/add/', methods=['GET', 'POST'])
def vlan_add():
	form = VlanEditForm(request.form)
	form.subnet_id.choices = [(i.id, i.name) for i in Subnet.query.all()]
	form.subnet_id.choices.insert(0, (0, u'- 指定子网 -'))
	if form.validate_on_submit():
		vlan = Vlan()
		form.populate_obj(vlan)
		db.session.add(vlan)
		db.session.commit()
		return redirect(url_for("subnet.vlan_list"))
	return render_template('subnet/vlan_edit.html', form=form)

@mod.route('/vlan/detail/<int:id>')
def vlan_detail(id):
    vlan = Vlan.query.filter_by(id=id).first()
    form = VlanDetailForm(request.form, vlan)
    form.subnet_id.choices = [(i.id, i.name) for i in Subnet.query.order_by(Subnet.id)] # pass choise option
    return render_template('subnet/vlan_detail.html', form=form)

@mod.route('/vlan/edit/<int:id>', methods=['GET', 'POST'])
def vlan_edit(id):
    vlan = Vlan.query.filter_by(id=id).first()
    form = VlanEditForm(request.form, vlan)
    form.subnet_id.choices = [(i.id, i.name) for i in Subnet.query.order_by(Subnet.id)] # pass choise option
    form.subnet_id.choices.insert(0, (0, u'- 指定子网 -'))
    if form.validate_on_submit():
        form.populate_obj(vlan)
        db.session.commit()
        return redirect(url_for('subnet.vlan_list')) 
    return render_template('subnet/vlan_edit.html', form=form)

@mod.route('/vlan/delete/<int:id>')
def vlan_delete(id):
	vlan = Vlan.query.filter_by(id=id).first()
	db.session.delete(vlan)
	db.session.commit()
	return redirect(url_for('subnet.vlan_list'))