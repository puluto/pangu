# -*- coding: utf-8 -*
from flask import Blueprint, render_template, flash, redirect, url_for, session, request, g, jsonify
from pangu import db, app
from pangu.datacenter.forms import LocationEditForm, LocationDetailForm, AreaEditForm, AreaDetailForm, \
	RackEditForm, RackDetailForm
from pangu.datacenter.models import Location, Area, Rack, Unit
from pangu.subnet.models import Vlan
from pangu.manufacture.models import Manufacture

mod = Blueprint('datacenter', __name__)

@mod.route('/location/')
def location_list():
	locations = db.session.query(Location, Manufacture) \
		.outerjoin(Manufacture, Location.manufacture_id == Manufacture.id).all()
	return render_template('datacenter/location_list.html', locations=locations)

@mod.route('/location/add/', methods=['GET', 'POST'])
def location_add():
	form = LocationEditForm(request.form)
	form.manufacture_id.choices = [(i.id, i.short_name) \
		for i in Manufacture.query.filter(Manufacture.supplier == True).all()]
	if form.validate_on_submit():
		location = Location()
		form.populate_obj(location)
		db.session.add(location)
		db.session.commit()
		return redirect(url_for("datacenter.location_list"))
	return render_template('datacenter/location_edit.html', form=form)

@mod.route('/location/detail/<int:id>')
def location_detail(id):
    location = Location.query.filter_by(id=id).first()
    form = LocationDetailForm(request.form, location)
    form.manufacture_id.choices = [(i.id, i.short_name) \
    	for i in Manufacture.query.filter(Manufacture.supplier == True).all()]
    return render_template('datacenter/location_detail.html', form=form)

@mod.route('/location/edit/<int:id>', methods=['GET', 'POST'])
def location_edit(id):
    location = Location.query.filter_by(id=id).first()
    form = LocationEditForm(request.form, location)
    form.manufacture_id.choices = [(i.id, i.short_name) \
    	for i in Manufacture.query.filter(Manufacture.supplier == True).all()]
    if form.validate_on_submit():
        form.populate_obj(location)
        db.session.commit()
        return redirect(url_for('datacenter.location_list')) 
    return render_template('datacenter/location_edit.html', form=form)

@mod.route('/location/delete/<int:id>')
def location_delete(id):
	location = Location.query.filter_by(id=id).first()
	db.session.delete(location)
	db.session.commit()
	return redirect(url_for('datacenter.location_list'))

@mod.route('/area/')
def area_list():
	areas = db.session.query(Area, Location) \
		.outerjoin(Location, Area.location_id == Location.id).all()
	return render_template('datacenter/area_list.html', areas=areas)

@mod.route('/area/add/', methods=['GET', 'POST'])
def area_add():
	form = AreaEditForm(request.form)
	form.location_id.choices = [(i.id, i.short_name) for i in Location.query.all()]
	if form.validate_on_submit():
		area = Area()
		form.populate_obj(area)
		db.session.add(area)
		db.session.commit()
		return redirect(url_for("datacenter.area_list"))
	return render_template('datacenter/area_edit.html', form=form)

@mod.route('/area/detail/<int:id>')
def area_detail(id):
    area = Area.query.filter_by(id=id).first()
    form = AreaDetailForm(request.form, area)
    form.location_id.choices = [(i.id, i.short_name) for i in Location.query.all()]
    return render_template('datacenter/area_detail.html', form=form)

@mod.route('/area/edit/<int:id>', methods=['GET', 'POST'])
def area_edit(id):
    area = Area.query.filter_by(id=id).first()
    form = AreaEditForm(request.form, area)
    form.location_id.choices = [(i.id, i.short_name) for i in Location.query.all()]
    if form.validate_on_submit():
        form.populate_obj(area)
        db.session.commit()
        return redirect(url_for('datacenter.area_list')) 
    return render_template('datacenter/area_edit.html', form=form)

@mod.route('/area/delete/<int:id>')
def area_delete(id):
	area = Area.query.filter_by(id=id).first()
	db.session.delete(area)
	db.session.commit()
	return redirect(url_for('datacenter.area_list'))

@mod.route('/area/json/select_list/') # get JSon of area select list
def area_selectlist():
	areas = Area.query.filter_by(location_id=request.args.get('choice', type=int))
	result	= [{'id': i.id, 'name': i.name} for i in areas]
	return jsonify(json=result)

def write_unit_table(units):
	rack = Rack.query.order_by(Rack.id.desc()).first()
	if rack is None:
		rack_id = 1
	else:
		rack_id = rack.id
	print rack_id
	db.session.execute(
		Unit.__table__.insert(),
		[{'name': i, 'rack_id': rack_id} for i in xrange(1, int(units)+1)]
	)
	db.session.commit()

@mod.route('/rack/')
def rack_list():
	racks = db.session.query(Rack, Location, Area) \
		.outerjoin(Location, Rack.location_id == Location.id) \
		.outerjoin(Area, Rack.area_id == Area.id) \
		.all()
	return render_template('datacenter/rack_list.html', racks=racks)

@mod.route('/rack/add/', methods=['GET', 'POST'])
def rack_add():
	form = RackEditForm(request.form)
	form.location_id.choices = [(i.id, i.short_name) for i in Location.query.all()]
	form.location_id.choices.insert(0, (0, u'- 指定机房 -'))
	form.area_id.choices = [(i.id, i.name) for i in Area.query.all()]
	form.area_id.choices.insert(0, (0, u'- 指定区域 -'))
	form.vlan_id.choices = [(i.id, i.name) for i in Vlan.query.all()]
	form.vlan_id.choices.insert(0, (0, u'- 指定vlan -'))
	
	if form.validate_on_submit():
		rack = Rack()
		form.populate_obj(rack)
		vlan_list = [str(i) for i in form.vlan_id.data]
		rack.vlan_id= ','.join(vlan_list)
		db.session.add(rack)
		db.session.commit()
		write_unit_table(form.units.data)
		flash(u'成功增加一条机柜记录!')
		return redirect(url_for("datacenter.rack_list"))
	return render_template('datacenter/rack_edit.html', form=form)

@mod.route('/rack/detail/<int:id>')
def rack_detail(id):
	rack = Rack.query.filter_by(id=id).first()
	units = Unit.query.filter(Unit.rack_id==rack.id).order_by(Unit.id.desc()).all()
	form = RackDetailForm(request.form, rack)
	form.location_id.choices = [(i.id, i.short_name) for i in Location.query.all()]
	form.area_id.choices = [(i.id, i.name) for i in Area.query.all()]
	vlans = [str(i) for i in rack.vlan_id.split(',')]
	form.vlan_id.choices = [(i.id, i.name) for i in Vlan.query.filter(Vlan.id.in_(vlans)).all()]
	return render_template('datacenter/rack_detail.html', form=form, units=units)

@mod.route('/rack/edit/<int:id>', methods=['GET', 'POST'])
def rack_edit(id):
	rack = Rack.query.filter_by(id=id).first()
	form = RackEditForm(request.form, rack)
	form.location_id.choices = [(i.id, i.short_name) for i in Location.query.all()]
	form.location_id.choices.insert(0, (0, u'- 指定机房 -'))
	form.area_id.choices = [(i.id, i.name) for i in Area.query.all()]
	form.area_id.choices.insert(0, (0, u'- 指定区域 -'))
	form.vlan_id.choices = [(i.id, i.name) for i in Vlan.query.all()]
	form.vlan_id.choices.insert(0, (0, u'- 指定vlan -'))

	if form.validate_on_submit():
		form.populate_obj(rack)
		vlan_list = [str(i) for i in form.vlan_id.data]
		rack.vlan_id = ','.join(vlan_list)
		db.session.commit()
		return redirect(url_for("datacenter.rack_list"))
	return render_template('datacenter/rack_edit.html', form=form)

@mod.route('/rack/delete/<int:id>')
def rack_delete(id):
	# 判断机柜中是否关联设备，如果没有删除，否则提示不能删除。涉及unit表
	rack = Rack.query.filter_by(id=id).first()
	db.session.query(Unit).filter(Unit.rack_id==rack.id).delete()
	db.session.delete(rack)
	db.session.commit()
	return redirect(url_for('datacenter.rack_list'))